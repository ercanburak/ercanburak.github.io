#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
from collections import namedtuple
import sys


def _print(args, text, **kwargs):
    if not args.quiet:
        print(text, **kwargs)


class Author(namedtuple("Author", ["name", "url"])):
    @property
    def is_me(self):
        return self.name == "Despoina Paschalidou"


class Paper(namedtuple("Paper", [
        "title",
        "url",
        "image",
        "authors",
        "conference",
        "year",
        "special",
        "links"
    ])):
    pass


class Conference(namedtuple("Conference", ["name"])):
    pass


class Link(namedtuple("Link", ["name", "url", "html", "text"])):
    pass


def author_list(authors, *names):
    return [authors[n] for n in names]


authors = {
    "bercan": Author("Burak Ercan", ""),
    "oeker": Author("Onur Eker", "https://github.com/ekeronur/"),
    "csaglam": Author("Canberk Saglam", "https://github.com/CanberkSaglam/"),
    "ae": Author("Aykut Erdem", "https://aykuterdem.github.io/"),
    "ee": Author("Erkut Erdem", "https://web.cs.hacettepe.edu.tr/~erkut/")
}
conferences = {
    "neurips": Conference("Advances in Neural Information Processing Systems (NeurIPS)"),
    "cvpr": Conference("Computer Vision and Pattern Recognition (CVPR)"),
    "cvprw": Conference("Computer Vision and Pattern Recognition (CVPR) Workshops"),
    "iccv": Conference("International Conference on Computer Vision (ICCV)"),
    "eusipco": Conference("European Signal Processing Conference (EUSIPCO)"),
    "acmmm": Conference("ACM Multimedia Conference (ACMM)"),
    "tmlr": Conference("Transactions on Machine Learning Research (TMLR)"),
    "pg": Conference("Pacific Graphics"),
    "arxiv": Conference("arXiv")
}
publications = [
    Paper(
        "HyperE2VID: Improving Event-Based Video Reconstruction via Hypernetworks",
        "https://ercanburak.github.io/HyperE2VID.html",
        "projects/HyperE2VID/detailed.png",
        author_list(authors, "bercan", "oeker", "csaglam", "ae", "ee"),
        conferences["arxiv"],
        2023,
        None,
        [Link("Abstract", None, "Event-based cameras are becoming increasingly popular for their ability to capture high-speed motion with low latency and high dynamic range. However, generating videos from events remains challenging due to the highly sparse and varying nature of event data. To address this, in this study, we propose HyperE2VID, a dynamic neural anetwork architecture for event-based video reconstruction. Our approach uses hypernetworks to generate per-pixel adaptive filters guided by a context fusion module that combines information from event voxel grids and previously reconstructed intensity images. We also employ a curriculum learning strategy to train the network more robustly. Our comprehensive experimental evaluations across various benchmark datasets reveal that HyperE2VID not only surpasses current state-of-the-art methods in terms of reconstruction quality but also achieves this with fewer parameters, reduced computational requirements, and accelerated inference times.", None),
         Link("Project page", "HyperE2VID.html", None, None),
         Link("Paper", "https://arxiv.org/pdf/2305.06382.pdf", None, None),
         Link("Code", "https://github.com/ercanburak/HyperE2VID", None, None),
         Link("Video", "https://www.youtube.com/watch?v=BWEV56-E0mE", None, None),
         Link("Bibtex", None, None,
              """@article{ercan2023hypere2vid,
  title={{HyperE2VID}: Improving Event-Based Video Reconstruction via Hypernetworks},
  author={Ercan, Burak and Eker, Onur and Saglam, Canberk and Erdem, Aykut and Erdem, Erkut},
  journal={arXiv preprint arXiv:2305.06382},
  year={2023}
}""")
        ]
    ),
    Paper(
        "EVREAL: Towards a Comprehensive Benchmark and Analysis Suite for Event-based Video Reconstruction",
        "https://ercanburak.github.io/evreal.html",
        "projects/evreal/diagram.png",
        author_list(authors, "bercan", "oeker", "ae", "ee"),
        conferences["cvprw"],
        2023,
        None,
        [Link("Abstract", None, "Event cameras are a new type of vision sensor that incorporates asynchronous and independent pixels, offering advantages over traditional frame-based cameras such as high dynamic range and minimal motion blur. However, their output is not easily understandable by humans, making the reconstruction of intensity images from event streams a fundamental task in event-based vision. While recent deep learning-based methods have shown promise in video reconstruction from events, this problem is not completely solved yet. To facilitate comparison between different approaches, standardized evaluation protocols and diverse test datasets are essential. This paper proposes a unified evaluation methodology and introduces an open-source framework called EVREAL to comprehensively benchmark and analyze various event-based video reconstruction methods from the literature. Using EVREAL, we give a detailed analysis of the state-of-the-art methods for event-based video reconstruction, and provide valuable insights into the performance of these methods under varying settings, challenging scenarios, and downstream tasks.", None),
         Link("Project page", "evreal.html", None, None),
         Link("Paper", "https://arxiv.org/pdf/2305.00434.pdf", None, None),
         Link("Code", "https://github.com/ercanburak/EVREAL", None, None),
         Link("Demo", "https://ercanburak-evreal.hf.space/", None, None),
         Link("Poster", "projects/evreal/poster.pdf", None, None),
         Link("Bibtex", None, None,
              """@inproceedings{ercan2023evreal,
  title={{EVREAL}: Towards a Comprehensive Benchmark and Analysis Suite for Event-based Video Reconstruction},
  author={Ercan, Burak and Eker, Onur and Erdem, Aykut and Erdem, Erkut},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={3942--3951},
  year={2023}
}""")
        ]
    ),
]


def build_publications_list(publications):
    def image(paper):
        if paper.image is not None:
            return '<img src="{}" alt="{}" />'.format(
                paper.image, paper.title
            )
        else:
            return '&nbsp;'

    def title(paper):
        return '<a href="{}">{}</a>'.format(paper.url, paper.title)

    def authors(paper):
        def author(author):
            if author.is_me:
                return '<strong class="author">{}</strong>'.format(author.name)
            else:
                return '<a href="{}" class="author">{}</a>'.format(
                    author.url, author.name
                )
        return ", ".join(author(a) for a in paper.authors)

    def conference(paper):
        cf = '{}, {}'.format(paper.conference.name, paper.year)
        if paper.special is not None:
            cf = cf + '<div class="special">   ({})</div>'.format(paper.special)
        return cf

    def links(paper):
        def links_list(paper):
            def link(i, link):
                if link.url is not None:
                    # return '<a href="{}">{}</a>'.format(link.url, link.name)
                    return '<a href="{}" data-type="{}">{}</a>'.format(link.url, link.name, link.name)
                else:
                    return '<a href="#" data-type="{}" data-index="{}">{}</a>'.format(link.name, i, link.name)
            return " ".join(
                link(i, l) for i, l in enumerate(paper.links)
            )

        def links_content(paper):
            def content(i, link):
                if link.url is not None:
                    return ""
                return '<div class="link-content" data-index="{}">{}</div>'.format(
                    i, link.html if link.html is not None
                       else '<pre>' + link.text + "</pre>"
                )
            return "".join(content(i, link) for i, link in enumerate(paper.links))
        return links_list(paper) + links_content(paper)

    def paper(p):
        return ('<div class="row paper">'
                    '<div class="image">{}</div>'
                    '<div class="content">'
                        '<div class="paper-title">{}</div>'
                        '<div class="conference">{}</div>'
                        '<div class="authors">{}</div>'
                        '<div class="links">{}</div>'
                    '</div>'
                '</div>').format(
                    image(p),
                    title(p),
                    conference(p),
                    authors(p),
                    links(p)
                )

    return "".join(paper(p) for p in publications)


def main(argv):
    parser = argparse.ArgumentParser(
        description="Create a publication list and insert in into an html file"
    )
    parser.add_argument(
        "file",
        help="The html file to insert the publications to"
    )

    parser.add_argument(
        "--safe", "-s",
        action="store_true",
        help="Do not overwrite the file but create one with suffix .new"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Do not output anything to stdout/stderr"
    )

    args = parser.parse_args(argv)

    # Read the file
    with open(args.file) as f:
        html = f.read()

    # Find the fence comments
    start_text = "<!-- start publication list -->"
    end_text = "<!-- end publication list -->"
    start = html.find(start_text)
    end = html.find(end_text, start)
    if end < start or start < 0:
        _print(args, "Could not find the fence comments", file=sys.stderr)
        sys.exit(1)

    # Build the publication list in html
    replacement = build_publications_list(publications)

    # Update the html and save it
    html = html[:start+len(start_text)] + replacement + html[end:]

    # If safe is set do not overwrite the input file
    if args.safe:
        with open(args.file + ".new", "w") as f:
            f.write(html)
    else:
        with open(args.file, "w") as f:
            f.write(html)


if __name__ == "__main__":
    main(None)
