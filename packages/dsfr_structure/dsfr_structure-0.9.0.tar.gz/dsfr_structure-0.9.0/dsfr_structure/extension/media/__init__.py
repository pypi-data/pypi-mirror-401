import xml.etree.ElementTree as etree

from pymdownx.blocks import BlocksExtension
from pymdownx.blocks.block import Block, type_string, type_string_in


class DsfrMedia(Block):
    NAME = "media"
    ARGUMENT = None
    OPTIONS = {
        "type": (
            "video",
            type_string_in(["video", "video_external", "audio", "image"]),
        ),
        "url": ("", type_string),
        "captions": ("", type_string),
        "title": ("", type_string),
        "poster": ("", type_string),
        "link": ("", type_string),
        "link_label": ("", type_string),
        "ratio": (
            "16x9",
            type_string_in(["16x9", "4x3", "1x1", "32x9", "3x2", "3x4", "2x3"]),
        ),
    }

    count = 0

    def on_create(self, parent):
        # <figure role="group" class="fr-content-media" aria-label="Description / Source">
        # ... contenu média ...
        #     <figcaption class="fr-content-media__caption">
        #         Vidéo d'explication des visio-conférences / Dnum 2024
        #     </figcaption>
        # </figure>

        media_id = "figure-%s" % DsfrMedia.count
        DsfrMedia.count += 1

        media_figure = etree.SubElement(parent, "figure")
        media_figure.set("role", "group")
        media_figure.set("id", media_id)
        media_figure.set("class", "fr-content-media")
        media_figure.set("aria-label", self.argument)

        match self.options["type"]:
            case "video":
                self._create_video(media_figure)
            case "video_external":
                self._create_video_iframe(media_figure)
            case "audio":
                self._create_audio(media_figure)
            case "image":
                self._create_image(media_figure)

        if self.argument:
            figcaption = etree.SubElement(media_figure, "figcaption")
            figcaption.set("class", "fr-content-media__caption")
            figcaption.text = self.argument

            if self.options["link"]:
                link = etree.SubElement(figcaption, "a")
                link.set("href", self.options["link"])
                link.set("class", "fr-link")
                link.set("id", f"{media_id}-link")
                link.text = (
                    self.options["link_label"]
                    if self.options["link_label"]
                    else self.options["link"]
                )

        return media_figure

    def _create_video(self, media_figure):
        #     <video src='https://aide.din.developpement-durable.gouv.fr/fichiers/Dnum.mp4' poster="../videos/video.png" class="fr-responsive-vid" controls>
        #         <track kind="captions" label="Francais" src="../videos/video.vtt" srclang="fr" default />
        #     </video>
        media_video = etree.SubElement(media_figure, "video")
        media_video.set("class", f"fr-responsive-vid  fr-ratio-{self.options['ratio']}")
        media_video.set("controls", "")
        if self.options["poster"]:
            media_video.set("poster", self.options["poster"])
        if self.options["url"]:
            media_video.set("src", self.options["url"])
        if self.options["captions"]:
            track = etree.SubElement(media_video, "track")
            track.set("kind", "captions")
            track.set("label", "Français")
            track.set("src", self.options["captions"])
            track.set("srclang", "fr")
            track.set("default", "")

    def _create_video_iframe(self, media_figure):
        # <iframe title="[À MODIFIER - titre de la vidéo]" class="fr-responsive-vid fr-ratio-1x1" src="https://www.youtube.com/embed/HyirpmPL43I" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        media_iframe = etree.SubElement(media_figure, "iframe")
        media_iframe.set(
            "class", f"fr-responsive-vid  fr-ratio-{self.options['ratio']}"
        )
        if self.options["url"]:
            media_iframe.set("src", self.options["url"])
        media_iframe.set(
            "allow", "accelerometer; encrypted-media; gyroscope; picture-in-picture"
        )
        media_iframe.set("allowfullscreen", "")
        media_iframe.set("title", self.get_title())

    def _create_audio(self, media_figure):
        #     <audio src='audio-file.mp3' class="fr-responsive-vid  fr-ratio-16x9" controls></audio>
        media_audio = etree.SubElement(media_figure, "audio")
        media_audio.set("class", f"fr-responsive-vid  fr-ratio-{self.options['ratio']}")
        media_audio.set("controls", "")
        if self.options["url"]:
            media_audio.set("src", self.options["url"])

    def _create_image(self, media_figure):
        # <div class="fr-content-media__img">
        #     <img class="fr-responsive-img" src="example/img/placeholder.16x9.png" alt="[À MODIFIER - vide ou texte alternatif de l’image]" />
        # </div>
        img_div = etree.SubElement(media_figure, "div")
        img_div.set("class", "fr-content-media__img")
        media_img = etree.SubElement(img_div, "img")
        media_img.set("class", f"fr-responsive-img  fr-ratio-{self.options['ratio']}")
        if self.options["url"]:
            media_img.set("src", self.options["url"])
            media_img.set("alt", self.get_title())

    def get_title(self):
        """Return the title."""
        if self.options["title"]:
            return self.options["title"]
        if self.argument:
            return self.argument
        return ""

    def _option(self, option):
        """Return the option value, ro empty string if not set."""
        if self.options[option]:
            return self.options[option]
        return ""

    def _option_bool(self, option, value):
        """Return the option value, or empty string if not set."""
        if self.options[option]:
            return value
        return ""


class DsfrMediaExtension(BlocksExtension):
    def extendMarkdownBlocks(self, md, block_mgr):
        block_mgr.register(DsfrMedia, self.getConfigs())


def makeExtension(*args, **kwargs):
    """Return extension."""

    return DsfrMediaExtension(*args, **kwargs)
