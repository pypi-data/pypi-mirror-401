# test.py
from xml.etree.ElementTree import fromstring, tostring

import markdown
from bs4 import BeautifulSoup

from dsfr_structure.extension.media import DsfrMediaExtension


def normalize_html(html: str) -> str:
    return tostring(fromstring(html)).decode()


def remove_whitespaces_and_indentations(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()


class TestMediaExtension:
    def setup_method(self):
        self.md = markdown.Markdown(extensions=[DsfrMediaExtension()])

    def test_case1(self):
        # given
        test_case = """
/// media | Vidéo d'explication des visio-conférences / Dnum 2024
    url: https://aide.din.developpement-durable.gouv.fr/fichiers/Dnum.mp4
    poster: ../videos/video.png
    captions: ../videos/video.vtt
    title: Example Image
///
"""
        expected_output = """
        <figure aria-label="Vidéo d'explication des visio-conférences / Dnum 2024" class="fr-content-media" id="figure-0" role="group">
            <video src='https://aide.din.developpement-durable.gouv.fr/fichiers/Dnum.mp4' poster="../videos/video.png" class="fr-responsive-vid fr-ratio-16x9" controls>
                <track kind="captions" label="Français" src="../videos/video.vtt" srclang="fr" default />
            </video>
            <figcaption class="fr-content-media__caption">
                Vidéo d'explication des visio-conférences / Dnum 2024
            </figcaption>
        </figure>
"""

        # when
        html_output = self.md.convert(test_case)

        html_output = remove_whitespaces_and_indentations(html_output)
        expected_output = remove_whitespaces_and_indentations(expected_output)

        # then
        assert expected_output == html_output

    def test_case2(self):
        # given
        test_case = """
/// media | Sample Audio
    type: audio
    title: Example Image
    url: https://example.com/audio.mp3
///
"""
        expected_output = """
        <figure aria-label="Sample Audio" class="fr-content-media" id="figure-1" role="group">
            <audio src='https://example.com/audio.mp3' class="fr-responsive-vid fr-ratio-16x9" controls></audio>
            <figcaption class="fr-content-media__caption">
                Sample Audio
            </figcaption>
        </figure>
"""
        # when
        html_output = self.md.convert(test_case)

        html_output = remove_whitespaces_and_indentations(html_output)
        expected_output = remove_whitespaces_and_indentations(expected_output)

        # then
        assert expected_output == html_output

    def test_case3(self):
        # given
        test_case = """
/// media | Sample Example Image
    type: image
    title: Example Image
    url: https://example.com/image.png
    ratio: 1x1
    link: https://example.com/
    link_label: Libellé du lien
///
"""
        expected_output = """
        <figure aria-label="Sample Example Image" class="fr-content-media" id="figure-2" role="group">
        <div class="fr-content-media__img">
            <img class="fr-responsive-img fr-ratio-1x1" src="https://example.com/image.png" alt="Example Image" />
        </div>

            <figcaption class="fr-content-media__caption">
                Sample Example Image
                <a id="figure-2-link" href="https://example.com/" class="fr-link">Libellé du lien</a>
            </figcaption>
        </figure>
"""
        # when
        html_output = self.md.convert(test_case)

        html_output = remove_whitespaces_and_indentations(html_output)
        expected_output = remove_whitespaces_and_indentations(expected_output)

        # then
        assert expected_output == html_output
