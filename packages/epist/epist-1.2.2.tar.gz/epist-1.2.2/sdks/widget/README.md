# Embeddable Search Widget

Add Epist.ai semantic search to any website with a single script.

## 1. Quick Start (HTML)

Drop this code where you want the widget to appear:

```html
<!-- Container -->
<div id="epist-widget" 
     data-api-key="YOUR_PUBLIC_KEY" 
     data-limit="5"
     data-placeholder="Search docs...">
</div>

<!-- Script -->
<script src="https://cdn.epist.ai/widget/v1/epist-widget.js"></script>
```

*(Note: Replace `cdn.epist.ai` with your actual CDN or host the file yourself)*

## 2. Configuration Options

| Attribute | Required | Default | Description |
|-----------|----------|---------|-------------|
| `data-api-key` | Yes | - | Your Epist.ai API Key |
| `data-limit` | No | 5 | Max results to show |
| `data-base-url`| No | https://api.epist.ai/v1 | Custom API endpoint |
| `data-placeholder` | No | "Ask a question..." | Search input placeholder |

## 3. Building from Source

To build the standalone `epist-widget.js`:

```bash
cd sdks/widget
npm install
npm run build:embed
```

Output will be in `dist/embed/epist-widget.js`.
