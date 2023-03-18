import { DataPoint } from "../../api/models";

type ParsedSupportingContentItem = {
    title: string;
    content: string;
};

export function parseSupportingContentItem(item: DataPoint): ParsedSupportingContentItem {
    // Assumes the item starts with the file name followed by : and the content.
    // Example: "sdp_corporate.pdf: this is the content that follows".
    // const parts = item.split(": ");
    // const title = parts[0];
    // const content = parts.slice(1).join(": ");

    // return {
    //     title,
    //     content
    // };
    return {
        title: item.source,
        content: item.content
    };
}
