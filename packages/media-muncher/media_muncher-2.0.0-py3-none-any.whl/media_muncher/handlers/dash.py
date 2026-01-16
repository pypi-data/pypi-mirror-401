from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Callable, Dict, List

from loguru import logger
from media_muncher.format import MediaFormat

from .xml import XMLHandler

if TYPE_CHECKING:
    from lxml import etree
    from mpd_inspector import MPDInspector
    from mpd_inspector.parser.mpd_tags import MPD


class DASHHandler(XMLHandler):
    media_format = MediaFormat.DASH
    content_types = ["application/dash+xml"]
    file_extensions = [".mpd"]

    uri_attributes = ["initialization", "media"]
    uri_elements = ["BaseURL"]

    def __init__(self, url, content: bytes | None = None, **kwargs):
        super().__init__(url, content, **kwargs)
        self._document: MPD = None

    @property
    def document(self) -> MPD:
        if not self._document:
            try:
                from mpd_inspector import MPDParser

                self._document = MPDParser.from_string(self.content.decode())
            except Exception as e:
                logger.error(f"Error parsing DASH document: {e}")
                raise e
        return self._document
        # return Parser.from_string(self.content.decode())

    @property
    def xml_document(self) -> etree._Element:
        from lxml import etree

        return etree.fromstring(self.content)

    @property
    def inspector(self) -> MPDInspector:
        from mpd_inspector import MPDInspector

        return MPDInspector(self.document)

    def read(self):
        return "Handling DASH file."

    @staticmethod
    def is_supported_content(content):
        try:
            from lxml import etree

            root = etree.fromstring(content)
            if root.tag == "{urn:mpeg:dash:schema:mpd:2011}MPD":
                return True
        except Exception as e:
            logger.error(f"Error parsing DASH document: {e}")
        return False

    def is_live(self):
        from mpd_inspector.parser.mpd_tags import PresentationType

        if self.document.type == PresentationType.DYNAMIC:
            return True
        else:
            return False

    def get_duration(self) -> float:
        """Extract duration from the MPD if it's for a VOD

        Returns:
            float: duration in seconds
        """
        if self.is_live():
            return -1
        else:
            return self.document.media_presentation_duration.total_seconds()

    def first_segment_url(self) -> str | None:
        urls = (
            self.inspector.periods[0]
            .adaptation_sets[0]
            .representations[0]
            .segment_information.full_urls("media")
        )
        if urls:
            return urls[0]

    def extract_features(self) -> Dict:
        info = {
            "format": "DASH",
            "type": "Live (dynamic)" if self.is_live() else "VOD (static)",
            "duration (in sec)": "N/A" if self.is_live() else self.get_duration(),
        }

        return info

    def extract_timeline(self):
        timeline = []

        for i, period in enumerate(self.inspector.periods):
            duration = period.duration
            if not duration and len(self.inspector.periods) > i + 1:
                duration = calculate_effective_duration(
                    period.start, self.inspector.periods[i + 1].start
                )

            info = {
                "period": period.id,
                "start": period_start_time(
                    self.document.availability_start_time, period.start
                ),
                "duration": duration,
                "baseUrl": period.base_urls[0].text if len(period.base_urls) else "",
            }
            timeline.append(info)

        return timeline

    def extract_structure(self) -> List[Dict] | None:
        features = []

        for period in self.document.periods:
            for adaptation_set in period.adaptation_sets:
                for representation in adaptation_set.representations:
                    res = (
                        "{} x {}".format(
                            representation.width,
                            representation.height,
                        )
                        if representation.width
                        else ""
                    )

                    features.append(
                        {
                            "period": period.id,
                            "adaptation_set": adaptation_set.id,
                            "type": adaptation_set.content_type,
                            "bandwidth": representation.bandwidth,
                            "codecs": representation.codecs or adaptation_set.codecs,
                            "resolution": res,
                            "language": adaptation_set.lang,
                        }
                    )

        return features

    def extract_facets(self) -> Dict:
        facets = {}

        features = {
            "DASH-Periods": lambda x: len(x.periods),
            "DASH-Events": lambda x: len(
                [event for period in x.periods for event in period.event_streams]
            ),
        }

        for key, value in features.items():
            try:
                facets[key] = value(self.document)
            except Exception:
                pass

        return {k: v for k, v in facets.items() if v is not None}

    def extract_digest(self) -> str:
        """Get a plain text digest summary of the MPD content.

        Returns:
            str: Plain text digest.
        """
        from media_muncher.handlers.generic import __version__

        lines = []

        # Add MPD-level annotations
        lines.append("~" * 60)

        # Extract key MPD attributes using inspector for computed values
        try:
            insp = self.inspector
            lines.append(
                f"Type: {'Live (dynamic)' if insp.is_live() else 'VOD (static)'}"
            )
            if insp.publish_time:
                lines.append(f"Publish Time: {insp.publish_time}")
            if insp.availability_start_time:
                lines.append(f"Availability Start Time: {insp.availability_start_time}")
            if insp.is_vod():
                lines.append(f"Duration: {self.get_duration()} seconds")
        except Exception as e:
            lines.append(f"Error extracting MPD info: {e}")

        # Add Period summaries
        try:
            insp = self.inspector
            lines.append("~" * 40)
            lines.append(f"Periods: {len(insp.periods)}")
            for i, period in enumerate(insp.periods):
                period_info = f"  Period {i + 1}: id={period.id}"
                if period.start_time:
                    period_info += f", start={period.start_time}"
                if period.duration:
                    period_info += f", duration={period.duration}"
                lines.append(period_info)

                # Count adaptation sets and representations
                num_as = len(period.adaptation_sets)
                num_rep = sum(len(a.representations) for a in period.adaptation_sets)
                lines.append(
                    f"    AdaptationSets: {num_as}, Representations: {num_rep}"
                )
        except Exception as e:
            lines.append(f"Error extracting period info: {e}")

        # Add closing line with version (aligned to 60 chars)
        version_suffix = f" media-muncher v{__version__} ~~"
        closing_line = "~" * (60 - len(version_suffix)) + version_suffix
        lines.append(closing_line)

        return "\n".join(lines)

    def annotate_content(self) -> bytes:
        """Annotate the MPD content with XML comments containing extracted metadata.

        Returns:
            bytes: The annotated MPD content with XML comments added.
        """
        from lxml import etree

        # Parse the XML
        parser = etree.XMLParser(remove_blank_text=False)
        root = etree.fromstring(self.content, parser=parser)

        # Get annotation lines and create XML comment
        # Note: XML comments cannot contain '--' so we use '~' for separators
        digest_lines = self.extract_digest().split("\n")
        comment_text = "\n" + "\n".join(digest_lines) + "\n"
        comment = etree.Comment(comment_text)

        # Insert comment at the beginning
        root.insert(0, comment)

        # Also add inline comments for each Period
        try:
            nsmap = root.nsmap
            ns = nsmap.get(None, "urn:mpeg:dash:schema:mpd:2011")

            for i, period_elem in enumerate(root.findall(f".//{{{ns}}}Period")):
                period_insp = self.inspector.periods[i]
                period_annotations = []
                period_annotations.append(f" Period: id={period_insp.id}")
                if period_insp.start_time:
                    period_annotations.append(f"start={period_insp.start_time}")
                if period_insp.duration:
                    period_annotations.append(f"duration={period_insp.duration}")

                period_comment = etree.Comment(
                    " " + ", ".join(period_annotations) + " "
                )
                period_elem.insert(0, period_comment)
        except Exception:
            pass  # Don't fail if inline comments can't be added

        # Return the annotated XML
        return etree.tostring(
            root, pretty_print=True, xml_declaration=True, encoding="UTF-8"
        )

    def get_update_interval(self) -> int | None:
        updateInterval = self.document.minimum_update_period
        return float(updateInterval.replace("PT", "").replace("S", ""))

    def download(
        self,
        output_path: str,
        num_segments: int,
        progress_callback: Callable[[str, int], None] | None = None,
    ):
        # Create the output path if it doesn't exist
        if output_path and not os.path.exists(output_path):
            os.makedirs(output_path)

        if num_segments > 0:
            raise NotImplementedError(
                "Downloading segments is not yet implemented for DASH"
            )

        # TODO - download segments
        total_tasks = 1
        if progress_callback:
            progress_callback(
                f"Number of files to download: {total_tasks}", total=total_tasks
            )

        main_filename = "main.mpd"
        local_file_path = os.path.join(output_path, main_filename)
        with open(local_file_path, "wb") as f:
            f.write(self.content)

        message = f"Downloaded MPD manifest to {local_file_path}"
        logger.info(message)
        if progress_callback:
            progress_callback(message)


def period_start_time(availability_start_time: str, start: str) -> str:
    if availability_start_time:
        availability_start_time_dt = datetime.fromisoformat(
            availability_start_time.replace("Z", "+00:00")
        )
        start_duration = float(start.replace("PT", "").replace("S", ""))
        start_time_dt = availability_start_time_dt + timedelta(seconds=start_duration)
        return start_time_dt.strftime("%Y-%m-%d %H:%M:%S")


def calculate_effective_duration(start_time, next_start_time):
    current_start = float(start_time.replace("PT", "").replace("S", ""))
    next_start = float(next_start_time.replace("PT", "").replace("S", ""))
    return next_start - current_start
