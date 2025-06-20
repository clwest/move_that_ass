# What Is This? Vision Identification

This feature lets you upload a hiking photo and receive a label and safety warning powered by OpenAI Vision.

## API Usage

```bash
curl -F "file=@snake.jpg" http://localhost:8000/api/vision/identify/
```
Response
```json
{"task_id": "<uuid>"}
```
Then poll `/api/core/tasks/<uuid>/` until you get:
```json
{"state": "SUCCESS", "data": "{\"label\":\"rattlesnake\",\"is_dangerous\":true,\"wiki_url\":\"https://en.wikipedia.org/...\"}"}
```

## UI

The Today page now has a purple camera button. Choose a photo or take one and you will see a sheet with the name, danger status and a link to Wikipedia.

