"""Render the static README sections in the same display style."""
from pathlib import Path
from roboto import outline
from html import escape
ROOT=Path(__file__).resolve().parents[1]
PANELS={
'work': ('01 / CURRENT WORK', [
'I build enterprise AI at Sentiment AI, where I own the',
'engineering stack for a behavioral analytics product.',
'',
'Voice agents & evaluation',
'PydanticAI · DSPy · RAGAS · Langfuse',
'',
'Long-context inference & model routing',
'H100 GPUs · LiteLLM · PyTorch',
'',
'Enterprise integrations & orchestration',
'Python · Temporal · Postgres']),
'asl':('03 / SELECTED WORK', ['Continuous ASL recognition >','ResNet18 + BiLSTM for sign recognition','from How2Sign video.']),
'paperbot':('PROJECT / PAPERBOT', ['Research-paper assistant >','LangChain · FAISS · GPT · Django','Pipeline optimization cut query time by 50%.']),
'portfolio':('PROJECT / E-INK PORTFOLIO', ['Explore the cube >','Three.js, monochrome dithering,','and keyboard navigation.']),
'research':('04 / RESEARCH', ['To BI or not To BI?','CAIT 2024 · December 2024','BERT reached 98.6% accuracy in the study.', '', 'PromptRefine','EAI ArtsIT · November 2025','Prompt refinement, evaluated across','OpenAI and Anthropic models.', '', 'Read about the research >']),
'education':('05 / BACKGROUND', ['BSc Computer Science · First Class Honours','Heriot-Watt University · 2025 · 4.0 GPA','UAE Golden Visa holder']),
}
for dark in [False,True]:
 theme='dark' if dark else 'light'; bg='#191919' if dark else '#ededeb'; fg='#fff' if dark else '#111'; line='#858581' if dark else '#777773'
 for key,(title,lines) in PANELS.items():
  height=98+len(lines)*34
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="840" height="{height}" viewBox="0 0 840 {height}" role="img"><title>{escape(title+". "+" ".join(lines))}</title><rect width="840" height="{height}" fill="{bg}"/><path d="M.5 0V{height}M839.5 0V{height}M28 .5H812" stroke="{line}"/><text x="28" y="40" font-family="monospace" font-size="18" fill="{fg}">{escape(title)}</text>'
  for i,value in enumerate(lines):
   svg+=f'<text x="28" y="{86+i*34}" font-family="Arial, Helvetica, sans-serif" font-size="24" fill="{fg}">{escape(value)}</text>'
  (ROOT/'assets'/f'{key}-{theme}.svg').write_text(outline(svg+'</svg>'))
 for key,label in [('website','PORTFOLIO >'),('resume','RESUME >'),('linkedin','LINKEDIN >'),('email','EMAIL >')]:
  (ROOT/'assets'/f'link-{key}-{theme}.svg').write_text(outline(f'<svg xmlns="http://www.w3.org/2000/svg" width="420" height="68" viewBox="0 0 420 68"><rect x=".5" y=".5" width="419" height="67" fill="{bg}" stroke="{line}"/><text x="24" y="43" font-family="Arial, Helvetica, sans-serif" font-size="24" fill="{fg}">{label}</text></svg>'))
