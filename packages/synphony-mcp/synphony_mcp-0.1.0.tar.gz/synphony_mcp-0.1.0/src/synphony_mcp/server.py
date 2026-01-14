"""Synphony MCP Server"""

import asyncio
from typing import Any, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import load_config
from .client import SynphonyClient


server = Server("synphony")
client: Optional[SynphonyClient] = None


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="datasets.list",
            description="List user's datasets with pagination",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of datasets to return",
                        "default": 20
                    },
                    "cursor": {
                        "type": "string",
                        "description": "Pagination cursor for next page"
                    }
                }
            }
        ),
        Tool(
            name="datasets.get",
            description="Get dataset details and file counts summary",
            inputSchema={
                "type": "object",
                "properties": {
                    "dataset_id": {
                        "type": "string",
                        "description": "Dataset ID"
                    }
                },
                "required": ["dataset_id"]
            }
        ),
        Tool(
            name="videos.search",
            description="Search and filter videos with pagination. Returns light metadata to help choose videos without extra calls.",
            inputSchema={
                "type": "object",
                "properties": {
                    "dataset_id": {
                        "type": "string",
                        "description": "Dataset ID to search within"
                    },
                    "stage": {
                        "type": "string",
                        "enum": ["original", "generated", "augmented"],
                        "description": "Filter by video type/stage"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "processing", "ready", "error"],
                        "description": "Filter by processing status"
                    },
                    "name": {
                        "type": "string",
                        "description": "Search for videos containing this text in their name (case-insensitive)"
                    },
                    "created_after": {
                        "type": "string",
                        "description": "ISO8601 timestamp - filter videos created after this time"
                    },
                    "created_before": {
                        "type": "string",
                        "description": "ISO8601 timestamp - filter videos created before this time"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of videos to return per page",
                        "default": 20
                    },
                    "cursor": {
                        "type": "string",
                        "description": "Pagination cursor for next page"
                    }
                },
                "required": ["dataset_id"]
            }
        ),
        Tool(
            name="videos.get",
            description="Get detailed information about a specific video, including processing state and progress",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_id": {
                        "type": "string",
                        "description": "Video ID"
                    }
                },
                "required": ["video_id"]
            }
        ),
        Tool(
            name="multiply.run",
            description="Generate video variations using AI prompts. Returns the IDs of newly created videos. Each input video is processed with each prompt to create variations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "dataset_id": {
                        "type": "string",
                        "description": "Dataset ID"
                    },
                    "input_video_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of input video IDs to process"
                    },
                    "prompts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of text prompts describing the desired video variations. Prompts should be simple, descriptive phrases about environmental conditions, weather, lighting, or scene modifications. Examples: 'rainy weather', 'snowy conditions', 'foggy morning', 'night time', 'bright sunny day', 'overcast sky'. Each video will be processed with each prompt."
                    },
                    "output_name_prefix": {
                        "type": "string",
                        "description": "Optional prefix for generated video names"
                    }
                },
                "required": ["dataset_id", "input_video_ids", "prompts"]
            }
        ),
        Tool(
            name="augment.run",
            description="Apply traditional computer vision augmentations to videos. Returns the IDs of newly created videos. Supported augmentations: RandomHorizontalFlip (horizontal flip), RandomRotation (rotate video), RandomAffine (affine transform), RandomPerspective (perspective warp), RandomResizedCrop (crop and resize), RandomGaussianNoise (add noise), ColorJitter (adjust brightness/contrast), RandomErasing (random occlusion).",
            inputSchema={
                "type": "object",
                "properties": {
                    "dataset_id": {
                        "type": "string",
                        "description": "Dataset ID"
                    },
                    "input_video_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of input video IDs to process"
                    },
                    "transforms": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "augName": {"type": "string"},
                                "augParams": {"type": "object"}
                            }
                        },
                        "description": "List of augmentations to apply. Format: [{'augName': '<name>', 'augParams': {...}}]. Available augNames: 'RandomHorizontalFlip' (params: p=probability 0-1, same_on_batch=0/1), 'RandomRotation' (params: p, degrees=rotation angle, resample='bilinear'/'nearest'), 'RandomAffine' (params: p, degrees), 'RandomPerspective' (params: p, distortion_scale=0-1, resample), 'RandomResizedCrop' (params: p, size=0-1), 'RandomGaussianNoise' (params: p, mean=0, std=1), 'ColorJitter' (params: p, brightness=1, contrast=1), 'RandomErasing' (params: p). Example: [{'augName': 'RandomHorizontalFlip', 'augParams': {'p': 0.5}}, {'augName': 'ColorJitter', 'augParams': {'p': 1, 'brightness': 1.2, 'contrast': 1.1}}]"
                    },
                    "output_name_prefix": {
                        "type": "string",
                        "description": "Optional prefix for augmented video names"
                    }
                },
                "required": ["dataset_id", "input_video_ids", "transforms"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    if client is None:
        return [TextContent(
            type="text",
            text="Error: MCP server not initialized. Check your config file."
        )]

    try:
        if name == "datasets.list":
            result = await handle_datasets_list(arguments)
        elif name == "datasets.get":
            result = await handle_datasets_get(arguments)
        elif name == "videos.search":
            result = await handle_videos_search(arguments)
        elif name == "videos.get":
            result = await handle_videos_get(arguments)
        elif name == "multiply.run":
            result = await handle_multiply_run(arguments)
        elif name == "augment.run":
            result = await handle_augment_run(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )]

        return [TextContent(type="text", text=str(result))]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error calling {name}: {str(e)}"
        )]


# Tool handlers (to be implemented)

async def handle_datasets_list(args: dict) -> dict:
    """List user's datasets"""
    limit = args.get("limit", 20)
    cursor = args.get("cursor")

    # Call API
    result = await client.list_datasets(limit=limit, cursor=cursor)

    # Transform response
    if not result.get("ok"):
        raise Exception(f"API error: {result.get('error', 'Unknown error')}")

    datasets = result.get("datasets", [])

    # TODO: Implement cursor pagination when backend supports it
    return {
        "datasets": datasets,
        "has_more": False  # No pagination yet
    }


async def handle_datasets_get(args: dict) -> dict:
    """Get dataset details"""
    dataset_id = args["dataset_id"]

    # Call API
    result = await client.get_dataset(dataset_id)

    # Transform response
    if not result.get("ok"):
        raise Exception(f"API error: {result.get('error', 'Unknown error')}")

    return {
        "dataset": result.get("dataset", {}),
        "summary": result.get("summary", {})
    }


async def handle_videos_search(args: dict) -> dict:
    """Search videos with filters"""
    dataset_id = args["dataset_id"]
    stage = args.get("stage")
    status = args.get("status")
    name = args.get("name")
    created_after = args.get("created_after")
    created_before = args.get("created_before")
    limit = args.get("limit", 20)
    cursor = args.get("cursor")

    # Call API
    result = await client.search_videos(
        dataset_id=dataset_id,
        stage=stage,
        status=status,
        name=name,
        created_after=created_after,
        created_before=created_before,
        limit=limit,
        cursor=cursor
    )

    # Transform response
    if not result.get("ok"):
        raise Exception(f"API error: {result.get('error', 'Unknown error')}")

    return {
        "videos": result.get("videos", []),
        "next_cursor": result.get("next_cursor"),
        "has_more": result.get("has_more", False)
    }


async def handle_videos_get(args: dict) -> dict:
    """Get video details"""
    video_id = args["video_id"]

    # Call API
    result = await client.get_video(video_id)

    # Transform response
    if not result.get("ok"):
        raise Exception(f"API error: {result.get('error', 'Unknown error')}")

    # Return video details
    return result


async def handle_multiply_run(args: dict) -> dict:
    """Run multiply processing"""
    dataset_id = args["dataset_id"]
    input_video_ids = args["input_video_ids"]
    prompts = args["prompts"]
    output_name_prefix = args.get("output_name_prefix")

    # Call API
    result = await client.multiply(
        dataset_id=dataset_id,
        input_video_ids=input_video_ids,
        prompts=prompts,
        output_name_prefix=output_name_prefix
    )

    # Transform response
    if not result.get("ok"):
        raise Exception(f"API error: {result.get('error', 'Unknown error')}")

    output_video_ids = result.get("output_video_ids", [])

    return {
        "output_video_ids": output_video_ids,
        "output_count": len(output_video_ids),
        "message": result.get("message", "Processing started"),
        "backend_status": result.get("backend_status")
    }


async def handle_augment_run(args: dict) -> dict:
    """Run augmentation processing"""
    dataset_id = args["dataset_id"]
    input_video_ids = args["input_video_ids"]
    transforms = args["transforms"]
    output_name_prefix = args.get("output_name_prefix")

    # Call API
    result = await client.augment(
        dataset_id=dataset_id,
        input_video_ids=input_video_ids,
        transforms=transforms,
        output_name_prefix=output_name_prefix
    )

    # Transform response
    if not result.get("ok"):
        raise Exception(f"API error: {result.get('error', 'Unknown error')}")

    output_video_ids = result.get("output_video_ids", [])

    return {
        "output_video_ids": output_video_ids,
        "output_count": len(output_video_ids),
        "message": result.get("message", "Processing started"),
        "backend_status": result.get("backend_status")
    }


async def async_main():
    """Async main entry point"""
    global client

    # Load config and initialize client
    config = load_config()
    client = SynphonyClient(
        api_key=config["api_key"],
        base_url=config["api_base_url"]
    )

    # Validate API key on startup
    try:
        auth_result = await client.validate_api_key()
        if not auth_result.get("ok"):
            raise ValueError(f"API key validation failed: {auth_result.get('error', 'Unknown error')}")
        user = auth_result.get("user", {})
        print(f"✓ Authenticated as {user.get('email', 'unknown')}", flush=True)
    except Exception as e:
        print(f"✗ API key validation failed: {e}", flush=True)
        raise

    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    """Sync entry point for console script"""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
