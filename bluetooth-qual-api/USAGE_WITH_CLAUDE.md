# Using the Bluetooth Qual API Skill with Claude

This guide explains how to set up and use the Bluetooth Qualification API skill with Claude in VS Code.

## Setup Instructions

### Where to Put the Skill

For Claude to find and use this skill, it needs to be in a specific location in your workspace:

```
your-project/
└── .claude/
    └── skills/
        └── bluetooth-qual-api/    ← The skill folder goes here
            ├── SKILL.md
            ├── scripts/
            ├── references/
            └── ...
```

**Important:** The skill folder should be at **`.claude/skills/bluetooth-qual-api/`** in your workspace root.

**Note:** This workspace currently has skills in `.github/skills/` which also works, but the standard Claude convention is `.claude/skills/`. You can use either location, but `.claude/skills/` is recommended for portability across different projects.

### Step-by-Step Setup

#### If You're Starting Fresh:

1. **Open your project in VS Code**
   - Open the folder where you want to use this skill
claude/skills/`
   - You can do this in VS Code's Explorer or in terminal:
     ```bash
     mkdir -p .claude/skills
     ```

3. **Copy the skill folder**
   - Copy the entire `bluetooth-qual-api` folder into `.claude/skills/`
   - Final path should be: `.claude/skills/bluetooth-qual-api/`

4. **Verify the structure**
   - Make sure `SKILL.md` is at: `.claude/skills/bluetooth-qual-api/SKILL.md`
   - This is the file Claude looks for to discover the skill

#### If This Skill Is Already in Your Workspace:

If you're reading this file and it's currently at `.github/skills/bluetooth-qual-api/`, you have two options:

**Option 1: Keep it where it is** (works fine)
- `.github/skills/` is recognized by Claude
- No action needed if it's already working

**Option 2: Move to standard location** (recommended)
- Move the folderclaude/skills/bluetooth-qual-api/SKILL.md`
   - (Or `.github/skills/bluetooth-qual-api/SKILL.md` if using that location) to `.claude/skills/bluetooth-qual-api/`
- This follows the standard Claude convention
- Better for sharing with other projects

To move it:
```bash
mkdir -p .claude/skills
mv .github/skills/bluetooth-qual-api .claude/skills/
```

Good news! If you're reading this file in VS Code and it's already at `.github/skills/bluetooth-qual-api/USAGE_WITH_CLAUDE.md`, then the skill is **already set up correctly**. You can skip to the "How to Verify" section below.

### How to Verify It's Working

1. **Check the file exiclaude/skills/bluetooth-qual-api/` (or `.github/skills/bluetooth-qual-api/`)
   - Look for: `.github/skills/bluetooth-qual-api/SKILL.md`
   - If you can see this file in VS Code Explorer, you're good!

2. **Test the skill**
   - Open a new chat with Claude in VS Code
   - Ask a simple question: **"Find Bluetooth certified products from Apple"**
   - If Claude uses the skill and returns results, it's working!

3. **Expected behavior**
   - Claude should automatically detect your question is about Bluetooth qualifications
   - Claude will run the Python script (`bluetooth_api_client.py`)
   - You'll see results from the Bluetooth SIG database

### No Configuration Needed!

Once the skill is in `.github/skills/bluetooth-qual-api/`, Claude automatically:
- ✅ Discovers the skill by reading `SKILL.md`
- ✅ Knows when to use it (based on the description in the frontmatter)
- ✅ Accesses the Python client and documentation
- ✅ Executes searches when you ask relevant questions

You don't need to:
- ❌ Configure any settings files
- ❌ Install any extensions
- ❌ Tell Claude to "aither: `.claude/skills/bluetooth-qual-api/SKILL.md` or `.github/skills/bluetooth-qual-api/SKILL.md`
- Make sure you're in the correct workspace (the folder containing `.claude/` or

### Installing Python Dependencies

The skill uses Python, so you'll need one dependency installed:

```bash
pip install requests
```

That's it! Claude will handle everything else automatically.

### Troubleshooting Setup

**Claude doesn't seem to use the skill:**
- Check the path is exactly: `.github/skills/bluetooth-qual-api/SKILL.md`
- Make sure you're in the correct workspace (the folder containing `.github/`)
- Try asking a more specific question: "Search the Bluetooth SIG database for iPhone"

**"Command not found" or Python errors:**
- Make sure Python 3 is installed: `python3 --version`
- Install the requests library: `pip install requests`

**Still not working?**
- Restart VS Code
- Open a new Claude chat window
- Verify the SKILL.md file has the correct frontmatter (name and description)

## What is This Skill?

This skill enables Claude to search the Bluetooth SIG (Special Interest Group) Qualified Products database. When you ask Claude about Bluetooth certified products, it will automatically use this skill to query the official database and provide you with accurate qualification information.

## How It Works

The skill is **automatically activated** when you ask Claude questions about:
- Bluetooth certified/qualified products
- Product qualification information
- Searching by company name, product name, or model number
- Bluetooth SIG database queries

You don't need to manually activate the skill or reference it - Claude will detect when your question relates to Bluetooth qualifications and use the skill automatically.

## Example Prompts

### Search by Company
```
"Find all Apple Bluetooth certified products"
"Show me Sony's qualified Bluetooth devices"
"What Bluetooth products has Qualcomm certified recently?"
```

### Search by Product Name
```
"Search for AirPods in the Bluetooth qualification database"
"Find iPhone Bluetooth certifications"
"Look up WH-1000XM6 headphones qualification info"
```

### Search by Model Number
```
"Look up qualification info for model A2342"
"Find Bluetooth certification for model QCC3086"
"What product is model A3258?"
```

### Get Latest Certifications
```
"What are the latest Bluetooth certified products from Samsung?"
"Show me recent Sony Bluetooth qualifications, sorted by date"
"Get the newest Qualcomm Bluetooth certifications"
```

### Multi-Criteria Searches
```
"Find Apple AirPods certifications"
"Search for Sony noise-canceling headphones in the Bluetooth database"
"Look up Qualcomm's Android 16 Bluetooth configurations"
```

## What Claude Can Do

When you use this skill, Claude can:

✅ **Search the database** by company, product, or model number  
✅ **Extract detailed information** including:
   - Product name and marketing name
   - Model number
   - Company/manufacturer
   - Qualification/publish date
   - Product description

✅ **Sort results** by date (newest first)  
✅ **Filter results** based on your criteria  
✅ **Present data** in a clear, readable format  
✅ **Handle large result sets** (up to 1000 results per query)

## Example Conversations

### Example 1: Simple Search

**You:** "Find Bluetooth certified products from Apple"

**Claude:** Claude will use the skill to search the database and present results like:
```
Found 27 Apple Bluetooth certified products:

1. iPhone 17 (Model: A3258)
   Qualified: October 2025
   
2. iPhone 16 Pro (Model: A3083)
   Qualified: April 2025
   
3. iPad (Model: A3354)
   Qualified: May 2025
...
```

### Example 2: Model Lookup

**You:** "What is model A2342?"

**Claude:** Will search and identify:
```
Model A2342: iPhone 12 Pro Max
Manufacturer: Apple Inc.
Qualification Date: December 27, 2020
Type: Smartphone
```

### Example 3: Latest Products

**You:** "Show me the latest Sony Bluetooth products, sorted by date"

**Claude:** Will search, sort by date, and show:
```
Latest Sony Bluetooth certifications:

1. Alpha 7 V Camera (ILCE-7M5/B) - December 2025
2. Xperia 10 VI (SO-52E) - October 2025
3. DualSense Controller (CFI-ZCT2W) - October 2025
...
```

### Example 4: JSON Output for Development

**You:** "Get me JSON data for Samsung Bluetooth products, limit to 5 results"

**Claude:** Will run the command with `--json` flag and provide structured data.

## Tips for Best Results

### Be Specific
- ✅ "Find Apple iPhone Bluetooth certifications"
- ❌ "Find phones"

### Use Official Names
- ✅ "Search for WH-1000XM6"
- ✅ "Look up Qualcomm Snapdragon"

### Specify if You Want Recent Results
- "Show me the latest..." 
- "Find recent..."
- "Sort by date..."

### Ask for Specific Fields
- "What's the model number for iPhone 17?"
- "When was model A2342 certified?"
- "Who manufactures model QCC3086?"

## Understanding the Results

Claude will provide:

**Company Name**: The manufacturer (e.g., "Apple Inc.", "Sony Group Corporation")

**Product Name**: The marketing/commercial name (e.g., "iPhone 16 Pro", "WH-1000XM6")

**Model Number**: The specific model identifier (e.g., "A3083", "YY2984")

**Qualification Date**: When the product was certified (e.g., "2025-04-30")

**Description**: Product category and details (e.g., "Smartphone", "Wireless Noise Canceling Headset")

## Advanced Usage

### Combining with Other Tasks

You can ask Claude to:
- "Find Sony headphones and save the results to a CSV file"
- "Search for Apple products and create a comparison table"
- "Get Qualcomm certifications and generate a report"
- "Look up model A2342 and show me similar products"

### Integration with Code

You can ask Claude to:
- "Write a script that checks if a model number is Bluetooth certified"
- "Create a function to get all products from a specific company"
- "Build a tool that monitors new certifications from my favorite brands"

## Behind the Scenes

When you ask a question, Claude:

1. **Detects** your question is about Bluetooth qualifications
2. **Activates** the bluetooth-qual-api skill
3. **Executes** the Python client (`bluetooth_api_client.py`)
4. **Queries** the official Bluetooth SIG API
5. **Processes** the results (extracts, filters, sorts)
6. **Presents** the information in a clear format

All of this happens automatically - you just ask your question naturally.

## API Details

The skill queries the official Bluetooth SIG Qualification API:
- **Endpoint**: https://qualificationapi.bluetooth.com
- **Public Access**: No authentication required
- **Data Source**: Official Bluetooth SIG database
- **Updated**: Real-time qualification data

## Troubleshooting

**"No results found"**
- Try a different spelling or search term
- The product might not be Bluetooth certified
- Try searching by company instead of product

**Slow responses**
- Large companies (Apple, Samsung) may take 30-45 seconds
- The API can be slow for certain queries
- Claude will wait up to 45 seconds before timing out

**Want more results?**
- Ask Claude to increase the limit: "Search for Apple with up to 100 results"
- Default is usually 10-20 for readability

## Getting Help

If you want to:
- See the Python client code: Ask "Show me the bluetooth_api_client.py code"
- Understand the API better: Ask "Explain how the Bluetooth qualification API works"
- Run custom queries: Ask "How can I search for specific criteria?"
- Get raw JSON data: Ask "Give me the raw API response for [query]"

## Summary

Just ask Claude your question naturally about Bluetooth certifications, and the skill will handle the rest! No special commands or syntax needed - Claude understands your intent and uses the skill automatically.

**Ready to try?** Ask Claude something like:
- "What Bluetooth products has [YourFavoriteCompany] certified?"
- "Find model [ModelNumber] in the Bluetooth database"
- "Show me the latest Bluetooth certifications"
