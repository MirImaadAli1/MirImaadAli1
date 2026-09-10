# Profile refresh

Proposed sidebar bio:
AI / Machine Learning Engineer at Sentiment AI. Building LLM systems, voice agents, and evaluation pipelines.

Location: Dubai, UAE
Website: https://portfolio-beta-nine-19h42szfbx.vercel.app

The current website portrait is assets/portrait.png. Header PNGs provide consistent portrait rendering in GitHub READMEs. The activity panels have light and dark variants.

scripts/dashboard.py uses only Python's standard library. It reads public GitHub data using GITHUB_TOKEN and writes both activity SVGs. The scheduled workflow requests repository contents write permission solely to commit generated assets. It does not request private repository data. Failed fetches leave the existing panels unchanged.

The calendar uses GitHub's reported contribution totals, which may include anonymized private contributions if enabled on the account. The language panel counts the primary language of each public original repository, excluding the profile repository and scuba-vision. It does not measure proficiency or hours worked.

For local rendering from a saved GraphQL response, set PROFILE_DATA_FILE to that JSON file. For a live refresh, set GITHUB_TOKEN in the environment and run python3 scripts/dashboard.py. Never commit a token.

To regenerate the static headers, install sharp locally without committing node_modules, then run node scripts/header.cjs.
