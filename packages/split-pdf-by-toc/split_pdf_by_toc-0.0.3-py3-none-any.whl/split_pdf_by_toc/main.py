from itertools import pairwise
import logging
from collections.abc import Sequence
import argparse
from dataclasses import dataclass
import pathlib
import re
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Destination
from typing import Protocol, cast, TypeAlias
from split_pdf_by_toc.sanitize import sanitize_filename

logger = logging.getLogger(__name__)


class Arguments(Protocol):
    pdf_path: pathlib.Path
    output_dir: pathlib.Path
    overlap: bool
    depth: int
    prefix: str
    filter: re.Pattern[str] | None
    add_number_prefix: bool


def setup_logging() -> None:
    import sys
    from split_pdf_by_toc.color_formatter import ColorFormatter

    handler = logging.StreamHandler(sys.stderr)
    use_color = sys.stderr.isatty()

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    handler.setFormatter(ColorFormatter(use_color))

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.INFO)
    root.addHandler(handler)


def regex_type(regex: str) -> re.Pattern[str]:
    try:
        return re.compile(regex)
    except re.error as e:
        raise argparse.ArgumentTypeError(f"Invalid regex: {e}")


@dataclass
class TocPage:
    title: str
    page: int
    level: int


NestedDestinations: TypeAlias = Destination | Sequence["NestedDestinations"]


def extract_toc_pages(
    outlines: Sequence[NestedDestinations], *, reader: PdfReader, level: int = 1
) -> list[TocPage]:
    toc_pages: list[TocPage] = []
    for item in outlines:
        if isinstance(item, Sequence):
            toc_pages.extend(extract_toc_pages(item, reader=reader, level=level + 1))
        else:
            page_number = reader.get_destination_page_number(item)

            if (
                page_number is not None
                and item.title is not None
                and (page := TocPage(title=item.title, page=page_number, level=level))
                not in toc_pages
            ):
                toc_pages.append(page)
            else:
                if page_number is None:
                    logger.warning(f"no page number for '{item.title}")
                elif item.title is None:
                    logger.warning("missing title for entry in TOC")
                else:
                    logger.warning(f"duplicate entry for '{item.title}'")

    return toc_pages


@dataclass
class SubDocument:
    title: str
    start_page_idx: int
    end_page_idx: int


def generate_document_partition(
    page_tocs: Sequence[TocPage],
    *,
    total_document_pages: int,
    let_overlap: bool = False,
) -> Sequence[SubDocument]:
    partition: Sequence[SubDocument] = [
        SubDocument(
            title=start.title,
            start_page_idx=start.page - 1
            if let_overlap and start.page > 1
            else start.page,
            end_page_idx=end.page + 1
            if let_overlap and end.page < total_document_pages
            else end.page,
        )
        for start, end in pairwise(page_tocs)
    ]

    # handle trailing toc entry (last heading - end of document)
    partition.append(
        SubDocument(
            title=page_tocs[-1].title,
            start_page_idx=page_tocs[-1].page
            if not let_overlap
            else page_tocs[-1].page - 1,
            end_page_idx=total_document_pages,
        )
    )

    return partition


def write_partition(
    pdf: PdfReader,
    partition: Sequence[SubDocument],
    *,
    output_dir: pathlib.Path,
    prefix: str = "",
    add_number_prefix: bool = False,
):
    number_prefix_padding = len(str(len(partition)))
    for idx, doc in enumerate(partition):
        filename = output_dir / sanitize_filename(
            ((str(idx + 1).zfill(number_prefix_padding) + "_") if add_number_prefix else "")
            + prefix
            + doc.title
            + ".pdf"
        )

        pdf_writer = PdfWriter()
        pdf_writer.append(pdf, pages=(doc.start_page_idx, doc.end_page_idx))

        with open(filename, "wb") as f:
            pdf_writer.write_stream(f)

        logger.info(
            f"wrote file {filename} (pages {doc.start_page_idx}-{doc.end_page_idx})"
        )


def main():
    parser = argparse.ArgumentParser(
        prog="split-pdf-by-toc", description="Splits a PDF by TOC markers."
    )

    _ = parser.add_argument("pdf_path", help="Set the input PDF", type=pathlib.Path)
    _ = parser.add_argument(
        "-o",
        "--output-dir",
        help="Set the output directory",
        default=".",
        type=pathlib.Path,
    )
    _ = parser.add_argument(
        "--overlap",
        help="If provided, let output pages overlap with each other.",
        action="store_true",
    )
    _ = parser.add_argument(
        "-d",
        "--depth",
        help="Set the maximum depth of TOC entries",
        type=int,
        default=1,
    )
    _ = parser.add_argument(
        "-f",
        "--filter",
        help="Only select TOC entries matching a filter",
        type=regex_type,
    )
    _ = parser.add_argument(
        "-p",
        "--prefix",
        help="Set a (user) prefix for the output files",
        type=str,
        default="",
    )
    _ = parser.add_argument(
        "-n",
        "--add-number-prefix",
        help="Set a numbered prefix",
        action="store_true",
        default=False,
    )

    args: Arguments = cast(Arguments, cast(object, parser.parse_args()))  # lol

    setup_logging()

    if not args.pdf_path.exists():
        logger.fatal("PDF file does not exist.")
        exit(1)

    if not args.output_dir.exists():
        logger.info(f"creating output path '{args.output_dir}'")

        args.output_dir.mkdir()

    reader = PdfReader(args.pdf_path)

    if not reader.outline:
        logger.fatal("document does not contain a TOC.")
        exit(1)

    toc_pages = extract_toc_pages(reader.outline, reader=reader)
    filtered_toc_pages = filter(
        lambda p: p.level <= args.depth
        and (not args.filter or args.filter.match(p.title)),
        toc_pages,
    )
    sorted_toc_pages = sorted(filtered_toc_pages, key=lambda p: (p.level, p.page))
    partition = generate_document_partition(
        sorted_toc_pages,
        let_overlap=args.overlap,
        total_document_pages=reader.get_num_pages(),
    )

    write_partition(
        reader,
        partition,
        output_dir=args.output_dir,
        prefix=args.prefix,
        add_number_prefix=args.add_number_prefix,
    )


if __name__ == "__main__":
    main()
