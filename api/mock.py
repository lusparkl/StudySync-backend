me = {
    "nickname": "Adam",
    "email": "adam@gmail.com",
    "avatar": "mock_file.png",
}

workspaces = [
    {
        "id": 1,
        "name": "Exams lockin",
        "description": "Get things done",
        "avatar": "mock_avatar_1.png",
        "deadline": "2026-05-20",
    },
    {
        "id": 2,
        "name": "Javascript lockin",
        "description": "Get things with Javascript done",
        "avatar": "mock_avatar_2.png",
        "deadline": "2026-06-03",
    },
    {
        "id": 3,
        "name": "Physics lockin",
        "description": "Get things with Physics done",
        "avatar": "mock_avatar_3.png",
        "deadline": "2026-06-18",
    },
]

tasks = [
    {
        "id": 1,
        "workspace_id": 1,
        "title": "Learn math",
        "description": "Repeat derivatives and limits",
        "status": "todo",
    },
    {
        "id": 2,
        "workspace_id": 1,
        "title": "Learn physics",
        "description": "Repeat mechanics formulas",
        "status": "in_progress",
    },
    {
        "id": 3,
        "workspace_id": 2,
        "title": "Build small fetch project",
        "description": "Practice async javascript",
        "status": "done",
    },
]

notes = [
    {
        "id": 1,
        "workspace_id": 1,
        "title": "Math note",
        "content": "Derivative of x^2 is 2x",
    },
    {
        "id": 2,
        "workspace_id": 2,
        "title": "JS note",
        "content": "Promise.all waits for all promises",
    },
]

activity = [
    {
        "id": 1,
        "workspace_id": 1,
        "type": "task",
        "text": "Started learning physics",
    },
    {
        "id": 2,
        "workspace_id": 1,
        "type": "note",
        "text": "Added math note",
    },
    {
        "id": 3,
        "workspace_id": 2,
        "type": "task",
        "text": "Finished small fetch project",
    },
]
