import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

def fetch_arxiv_papers(query="cat:cs.CL OR cat:cs.LG", max_results=5):
    """Fetches real live research paper metadata directly from arXiv API."""
    # Encode query string to safely handle spaces and special characters
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    
    print(f"Connecting to live tool: {url}...")
    
    # Custom User-Agent header prevents arXiv API request blocks
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()
    
    # Parse XML payload
    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    papers = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
        link = entry.find('atom:id', ns).text.strip()
        published = entry.find('atom:published', ns).text.strip()[:10]
        
        papers.append({
            "title": title,
            "published": published,
            "link": link,
            "summary": summary[:300] + "..."
        })
    return papers

def run_research_scout_agent():
    print("=== STARTING ML RESEARCH SCOUT AGENT ===")
    
    # Fetch live data
    papers = fetch_arxiv_papers(max_results=3)
    
    if not papers:
        print("No new papers found.")
        return
    
    print(f"\nSuccessfully retrieved {len(papers)} live papers from arXiv API.")
    
    # Format Digest
    digest = "# 🤖 Weekly ML & AI Research Scout Digest\n\n"
    digest += "## 📌 High Priority & Relevant Papers\n\n"
    
    for idx, paper in enumerate(papers, 1):
        digest += f"### {idx}. {paper['title']}\n"
        digest += f"- **Published Date:** {paper['published']}\n"
        digest += f"- **ArXiv Link:** [{paper['link']}]({paper['link']})\n"
        digest += f"- **Abstract Snapshot:** {paper['summary']}\n\n"
        digest += "---\n"
        
    output_path = "weekly_research_digest.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(digest)
        
    print(f"\n[SUCCESS] Agent completed end-to-end run. Digest written to {output_path}")

if __name__ == "__main__":
    run_research_scout_agent()