import os
import pandas as pd
from datetime import datetime
import re
import json # To embed translations into HTML
import html # To escape model names safely for data attributes

# --- Model to Organization Mapping ---
# (Keep the existing model_to_organization dictionary)
model_to_organization = {
    "claude-3.5-haiku": "Anthropic",
    "claude-3.5-sonnet-20240620": "Anthropic",
    "claude-3.5-sonnet": "Anthropic",
    "claude-3.7-sonnet": "Anthropic",
    "command-r-08-2024": "Cohere",
    "command-r-plus-08-2024": "Cohere",
    "command-r7b-12-2024": "Cohere",
    "deepseek-v3": "Deepseek",
    "gemini-2.0-flash-001": "Google",
    "gemini-2.0-flash-lite-001": "Google",
    "gemma-2-27b-it": "Google",
    "gemma-2-9b-it": "Google",
    "gpt-4.5-preview": "OpenAI",
    "gpt-4o-2024-11-20": "OpenAI",
    "gpt-4-1106-preview": "OpenAI",
    "gpt-4o-mini": "OpenAI",
    "grok-2-1212": "xAI",
    "hermes-3-llama-3.1-405b": "NousResearch",
    "hermes-3-llama-3.1-70b": "NousResearch",
    "lfm-3b": "Liquid AI",
    "lfm-40b": "Liquid AI",
    "lfm-7b": "Liquid AI",
    "llama-3.1-405b-instruct": "Meta",
    "llama-3.1-70b-instruct": "Meta",
    "llama-3.1-8b-instruct": "Meta",
    "llama-3.1-nemotron-70b-instruct": "Meta",
    "llama-3.3-70b-instruct": "Meta",
    "minimax-01": "MiniMax",
    "mistral-large-2411": "Mistral",
    "mistral-small-24b-instruct-2501": "Mistral",
    "nova-lite-v1": "Amazon",
    "nova-micro-v1": "Amazon",
    "nova-pro-v1": "Amazon",
    "qwen2.5-32b-instruct": "Alibaba",
    "wizardlm-2-8x22b": "Microsoft",
    "o3-mini-high": "OpenAI",
    "o3-mini-medium": "OpenAI",
    "o3-mini-low": "OpenAI",
    "qwen-2.5-72b-instruct": "Alibaba",
    "qwen-2.5-7b-instruct": "Alibaba",
    "o1-medium": "OpenAI",
    "o1-low": "OpenAI",
    "gemma-3-27b-it": "Google",
    "jamba-1.6-large": "AI21",
    "jamba-1.6-mini": "AI21",
    "command-a": "Cohere",
    "olmo-2-0325-32b-instruct": "Allen AI",
    "mistral-small-3.1-24b-instruct-2503": "Mistral",
    "o1-high": "OpenAI",
    "deepseek-chat-v3-0324": "Deepseek",
    "deepseek-r1": "Deepseek",
    "gemini-2.0-flash-thinking-exp-01-21": "Google",
    "gemini-2.0-pro-exp-02-05": "Google",
    "gemini-2.5-pro-exp-03-25": "Google",
    "chatgpt-4o-latest(2025-03-26)": "OpenAI",
    "qwq-32b": "Alibaba",
    "claude-3.7-sonnet(thinking)": "Anthropic",
    "qwen-turbo": "Alibaba",
    "qwen-plus": "Alibaba",
    "qwen-max": "Alibaba",
    "grok-3-beta": "xAI",
    "grok-3-mini-beta": "xAI",
}

# --- Translation Data ---
# (Keep the existing translations dictionary)
translations = {
    'ko': {
        'title': "Ko-Arena-Hard 리더보드 ({{update_date}})",
        'heading': "Ko-Arena-Hard-Auto 리더보드 ({{update_date}})",
        'notice': '<strong style="color: var(--judge-color-text)">주의:</strong> judge 모델(gemini-2.0-flash, gpt-4o-mini, deepseek-chat-v3-0324)은 자체 답변 선호 경향으로 인해 실제 성능보다 점수가 높게 나타날 수 있습니다. 해당 모델들의 점수 해석 시 유의하시기 바랍니다.', # Use variable for strong color
        'select_leaderboard_label': "리더보드 선택:",
        'select_language_label': "Select Language:",
        'search_placeholder': "모델명 검색...",
        'lang_ko': "한국어",
        'lang_en': "English",
        'col_rank': "순위",
        'col_org': "기관",
        'col_model': "모델",
        'col_score': "점수 (CI)",
        'col_elo': "Elo 점수 (CI)",
        'col_tokens': "평균 토큰",
        'lb_type_no_control': "컨트롤 없음",
        'lb_type_markdown_control': "마크다운 컨트롤",
        'lb_type_length_control': "길이 컨트롤",
        'lb_type_style_control': "스타일 컨트롤 (마크다운 + 길이)",
    },
    'en': {
        'title': "Ko-Arena-Hard Leaderboard ({{update_date}})",
        'heading': "Ko-Arena-Hard-Auto Leaderboard ({{update_date}})",
        'notice': '<strong style="color: var(--judge-color-text)">Caution:</strong> Judge models (gemini-2.0-flash, gpt-4o-mini, deepseek-chat-v3-0324) may show inflated scores due to self-preference bias. Please interpret their scores with caution.', # Use variable for strong color
        'select_leaderboard_label': "Select Leaderboard:",
        'select_language_label': "Select Language:",
        'search_placeholder': "Search model name...",
        'lang_ko': "한국어",
        'lang_en': "English",
        'col_rank': "Rank",
        'col_org': "Organization",
        'col_model': "Model",
        'col_score': "Score (CI)",
        'col_elo': "Elo Score (CI)",
        'col_tokens': "Avg Tokens",
        'lb_type_no_control': "No Control",
        'lb_type_markdown_control': "Markdown Control",
        'lb_type_length_control': "Length Control",
        'lb_type_style_control': "Style Control (Markdown + Length)",
    }
}

# --- Helper Functions ---

# (Keep get_latest_leaderboard_dir and process_leaderboard_csv as is)
def get_latest_leaderboard_dir(base_directory: str) -> tuple[str, str]:
    dir_pattern = re.compile(r"arena_hard_leaderboard_(\d{8})_ensemble")
    latest_date = None
    latest_dir = None
    if not os.path.isdir(base_directory): raise FileNotFoundError(f"Base directory not found: {base_directory}")
    for dirname in os.listdir(base_directory):
        full_path = os.path.join(base_directory, dirname)
        if os.path.isdir(full_path):
            match = dir_pattern.match(dirname)
            if match:
                date_str = match.group(1)
                try: dir_date = datetime.strptime(date_str, "%Y%m%d")
                except ValueError: print(f"Skipping directory with unexpected date format: {dirname}"); continue
                if latest_date is None or dir_date > latest_date: latest_date, latest_dir = dir_date, full_path
    if latest_dir is None: raise FileNotFoundError(f"No leaderboard directory found in {base_directory} matching the pattern 'arena_hard_leaderboard_YYYYMMDD_ensemble'")
    update_date_str = os.path.basename(latest_dir).split('_')[3]
    update_date = datetime.strptime(update_date_str, "%Y%m%d").strftime("%Y-%m-%d")
    return latest_dir, update_date

def process_leaderboard_csv(csv_path: str) -> pd.DataFrame | None:
    if not os.path.exists(csv_path): print(f"Warning: CSV file not found: {csv_path}"); return None
    try:
        df = pd.read_csv(csv_path)
        df['original_model'] = df['model']
        df = df.sort_values(by='score', ascending=False).reset_index(drop=True); df.index += 1; df.insert(0, 'Rank', df.index)
        model_map = {'claude-3.7-sonnet': 'claude-3.7-sonnet (baseline)', 'gemini-2.0-flash-001': 'gemini-2.0-flash-001 (judge)', 'gpt-4o-mini': 'gpt-4o-mini (judge)', 'deepseek-chat-v3-0324': 'deepseek-chat-v3-0324 (judge)'}
        df['model_display'] = df['model'].replace(model_map)
        df["organization"] = df["model"].map(model_to_organization).fillna("Unknown")
        def style_model(name: str) -> str:
            # Use CSS variables defined in the <style> block
            if "(judge)" in name: return f'<span class="model-tag model-judge">{html.escape(name)}</span>'
            if "(baseline)" in name: return f'<span class="model-tag model-baseline">{html.escape(name)}</span>'
            return html.escape(name)
        df['model_display'] = df['model_display'].apply(style_model)
        df['score_numeric'] = df['score']
        df['elo_numeric'] = pd.to_numeric(df['elo_score'], errors='coerce').fillna(0)
        df['avg_tokens_numeric'] = df['avg_tokens'].astype(int)
        df['avg_tokens_display'] = df['avg_tokens'].astype(int)
        df['CI'] = df['CI'].fillna(''); df['score_display'] = df['score'].round(2).astype(str) + df['CI']
        df['elo_CI'] = df['elo_CI'].fillna(''); df['elo_score_display'] = df['elo_numeric'].round(0).astype(int).astype(str) + df['elo_CI']
        df_display = df[['Rank', 'model_display', 'original_model', 'organization', 'score_display', 'score_numeric', 'elo_score_display', 'elo_numeric', 'avg_tokens_display', 'avg_tokens_numeric']].copy()
        df_display.rename(columns={'Rank': 'col_rank', 'model_display': 'col_model', 'organization': 'col_org', 'score_display': 'col_score', 'elo_score_display': 'col_elo', 'avg_tokens_display': 'col_tokens'}, inplace=True)
        df_html = df_display[['col_rank', 'col_model', 'col_org', 'col_score', 'col_elo', 'col_tokens', 'original_model', 'score_numeric', 'elo_numeric', 'avg_tokens_numeric']]
        return df_html
    except Exception as e: print(f"Error processing CSV {csv_path}: {e}"); import traceback; traceback.print_exc(); return None


# --- MODIFIED FUNCTION ---
def generate_table_html(df: pd.DataFrame) -> str:
    numeric_cols = ['col_rank', 'col_score', 'col_elo', 'col_tokens']
    header_keys = ['col_rank', 'col_model', 'col_org', 'col_score', 'col_elo', 'col_tokens']
    data_value_map = {'col_rank': 'col_rank', 'col_model': 'original_model', 'col_org': 'col_org', 'col_score': 'score_numeric', 'col_elo': 'elo_numeric', 'col_tokens': 'avg_tokens_numeric'}
    html_string = '<table class="leaderboard-table" border="0">\n<thead>\n<tr>\n'
    for key in header_keys:
        sort_type = 'numeric' if key in numeric_cols else 'text'
        # The actual text content will be set by JavaScript using translations
        html_string += f'<th class="sortable" data-col-key="{key}" data-sort-type="{sort_type}">{key}</th>\n'
    html_string += '</tr>\n</thead>\n<tbody>\n'
    for _, row in df.iterrows():
        escaped_model_name = html.escape(row['original_model'], quote=True)
        html_string += f'<tr data-model-name="{escaped_model_name.lower()}">\n'
        for key in header_keys:
            display_value = row[key]
            data_col = data_value_map[key]
            data_value = row[data_col]
            # Ensure data_value is properly escaped for the attribute
            data_value_attr = html.escape(str(data_value), quote=True)

            # --- Add medal emojis for Rank column display ---
            cell_content = display_value # Default content is the original display value
            if key == 'col_rank':
                rank_num = row[key] # Get the actual numeric rank
                if rank_num == 1:
                    cell_content = f'🥇' # Prepend gold medal
                elif rank_num == 2:
                    cell_content = f'🥈' # Prepend silver medal
                elif rank_num == 3:
                    cell_content = f'🥉' # Prepend bronze medal
                # For ranks > 3, cell_content remains the original rank number
            # --- End medal emoji logic ---

            # Use the modified cell_content for display, but keep original data_value for sorting
            html_string += f'<td data-sort-value="{data_value_attr}">{cell_content}</td>\n'
        html_string += '</tr>\n'
    html_string += '</tbody>\n</table>'
    return html_string
# --- END MODIFIED FUNCTION ---


# --- Main Execution ---
if __name__ == '__main__':
    try:
        # (Keep directory setup and loop as is)
        leaderboard_base_dir = './leaderboard/'
        latest_dir, update_date = get_latest_leaderboard_dir(leaderboard_base_dir)
        print(f"Using latest leaderboard directory: {latest_dir}")
        print(f"Leaderboard update date: {update_date}")

        output_dir = 'dist'
        os.makedirs(output_dir, exist_ok=True)
        output_html_path = os.path.join(output_dir, 'leaderboard.html')

        leaderboard_types = [
            {'id': 'style-control', 'filename': 'style_control.csv', 'translate_key': 'lb_type_style_control'},
            {'id': 'markdown-control', 'filename': 'markdown_control.csv', 'translate_key': 'lb_type_markdown_control'},
            {'id': 'length-control', 'filename': 'length_control.csv', 'translate_key': 'lb_type_length_control'},
            {'id': 'no-control', 'filename': 'no_control.csv', 'translate_key': 'lb_type_no_control'},
        ]

        processed_data = {}
        leaderboard_dropdown_options_html = ""
        table_containers_html = ""
        default_leaderboard_id = 'style-control'
        default_lang = 'ko'

        for lb_type in leaderboard_types:
            csv_path = os.path.join(latest_dir, lb_type['filename'])
            df_processed = process_leaderboard_csv(csv_path)
            if df_processed is not None:
                # Use the MODIFIED generate_table_html function
                table_html = generate_table_html(df_processed)
                processed_data[lb_type['id']] = {'translate_key': lb_type['translate_key'], 'table_html': table_html}
                selected_attr = ' selected' if lb_type['id'] == default_leaderboard_id else ''
                # Text content will be set by JS
                leaderboard_dropdown_options_html += f'<option value="{lb_type["id"]}" data-translate-key="{lb_type["translate_key"]}"{selected_attr}></option>\n'
                display_style = 'block' if lb_type['id'] == default_leaderboard_id else 'none'
                table_containers_html += f"""<div class="table-container" id="table-{lb_type['id']}" data-id="{lb_type['id']}" style="display: {display_style};">{table_html}</div>"""
            else: print(f"Skipping leaderboard type '{lb_type['translate_key']}' due to missing or invalid CSV.")

        if not processed_data: raise ValueError(f"No valid leaderboard CSV files found in {latest_dir}")

        # --- Generate Dropdown/Search HTML ---
        # (Keep this section as is)
        language_dropdown_html = f"""
          <label for="language-select" data-translate-key="select_language_label"></label>
          <select id="language-select">
            <option value="ko" data-translate-key="lang_ko"{' selected' if default_lang == 'ko' else ''}></option>
            <option value="en" data-translate-key="lang_en"{' selected' if default_lang == 'en' else ''}></option>
          </select>
        """
        search_input_html = f"""
         <input type="text" id="model-search-input" placeholder="" data-translate-key-placeholder="search_placeholder">
        """
        translations_json = json.dumps(translations, ensure_ascii=False, indent=None)


        # --- HTML Template ---
        # (Keep the HTML template string as is, including the <style> block)
        html_template = """
        <!DOCTYPE html>
        <html lang="{default_lang}">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title data-translate-key="title"></title>
          <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
          <style>
            /* --- Professional Frontend/Artist CSS Enhancements --- */
            :root {{
              --primary-color: #00796b; /* Teal */
              --primary-darker: #004d40;
              --secondary-color: #ffffff; /* White */
              --accent-color: #ffc107; /* Amber */
              --text-color: #212529; /* Dark Gray - Good contrast */
              --text-muted: #6c757d; /* Medium Gray */
              --light-gray: #f8f9fa; /* Very Light Gray */
              --medium-gray: #e9ecef; /* Light Gray */
              --border-color: #dee2e6; /* Standard Border Gray */
              --judge-color-border: #e3342f; /* Red */
              --judge-color-text: #cc1f1a;
              --judge-bg: #fcebea;
              --baseline-color-border: #3490dc; /* Blue */
              --baseline-color-text: #2779bd;
              --baseline-bg: #eaf4fc;
              --border-radius: 6px;
              --box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
              --box-shadow-focus: 0 0 0 3px rgba(0, 121, 107, 0.25); /* Focus shadow using primary color */
              --input-bg: #fff;
              --sort-indicator-active: var(--primary-color);
              --sort-indicator-inactive: #adb5bd; /* Lighter gray for inactive arrows */
            }}

            /* --- Base & Layout --- */
            *, *::before, *::after {{ box-sizing: border-box; }}

            body {{
              font-family: 'Noto Sans KR', 'Roboto', sans-serif;
              background-color: var(--light-gray);
              margin: 0;
              padding: 25px 15px; /* More vertical padding */
              color: var(--text-color);
              line-height: 1.6;
              -webkit-font-smoothing: antialiased;
              -moz-osx-font-smoothing: grayscale;
            }}

            .container {{
              max-width: 1200px; /* Slightly wider */
              margin: 20px auto;
              background: var(--secondary-color);
              padding: 40px 50px; /* Generous padding */
              border-radius: var(--border-radius);
              box-shadow: var(--box-shadow);
              border: 1px solid var(--border-color);
            }}

            /* --- Typography --- */
            h1 {{
              text-align: center;
              margin-top: 0;
              margin-bottom: 35px; /* More space below heading */
              color: var(--primary-darker);
              font-weight: 700;
              font-size: 2.4em; /* Larger heading */
            }}
            h1 a {{ color: inherit; text-decoration: none; transition: color 0.3s ease; }}
            h1 a:hover {{ color: var(--primary-color); }}

            /* --- Controls (Dropdowns, Search) --- */
            .controls-container {{
                display: grid;
                /* Responsive columns: 2 cols default, 1 col on smaller screens */
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px 30px; /* Row and column gap */
                margin-bottom: 30px;
                align-items: end; /* Align items to the bottom of the grid cell */
            }}

            .control-group {{
                display: flex;
                flex-direction: column;
                gap: 8px; /* Space between label and input/select */
            }}

            .control-group label {{
                font-weight: 700;
                color: var(--text-muted);
                font-size: 0.8em; /* Smaller label */
                letter-spacing: 0.05em;
                padding-left: 2px; /* Slight indent */
            }}

            /* Common style for select and text input */
            .control-group select,
            .control-group input[type="text"] {{
                padding: 12px 15px; /* Comfortable padding */
                border-radius: var(--border-radius);
                border: 1px solid var(--border-color);
                font-size: 1rem; /* Standard input font size */
                font-family: inherit;
                width: 100%;
                background-color: var(--input-bg);
                transition: border-color 0.2s ease, box-shadow 0.2s ease;
                color: var(--text-color);
                appearance: none; /* Remove default styling */
                -webkit-appearance: none;
                -moz-appearance: none;
            }}

             /* Style placeholder text */
            .control-group input[type="text"]::placeholder {{
                color: var(--text-muted);
                opacity: 0.7;
            }}

            /* Custom dropdown arrow */
            .control-group select {{
                cursor: pointer;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='none' stroke='%236c757d' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3E%3C/svg%3E");
                background-repeat: no-repeat;
                background-position: right 15px center;
                background-size: 1em;
                padding-right: 40px; /* Space for arrow */
            }}

            /* Focus styles */
            .control-group select:focus,
            .control-group input[type="text"]:focus {{
                outline: none;
                border-color: var(--primary-color);
                box-shadow: var(--box-shadow-focus);
            }}

            /* --- Notice --- */
            .notice {{
              background-color: var(--judge-bg);
              color: var(--judge-color-text); /* Use specific text color for better contrast */
              border-left: 5px solid var(--judge-color-border);
              padding: 15px 20px;
              margin-bottom: 30px;
              border-radius: var(--border-radius);
              font-size: 0.95em;
            }}
            /* Strong tag color already set via variable in translation */

            /* --- Search Container --- */
            .search-container {{
                margin-bottom: 30px;
                max-width: 450px; /* Limit width */
            }}
            /* No label needed here */
            .search-container .control-group {{ gap: 0; }}


            /* --- Table Styling --- */
            .table-container {{
                overflow-x: auto; /* Essential for responsiveness */
                -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
                margin-top: 0;
                border: 1px solid var(--border-color);
                border-radius: var(--border-radius);
                box-shadow: 0 2px 6px rgba(0,0,0,0.05); /* Subtle shadow on container */
            }}

            .leaderboard-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 0.95rem; /* Slightly larger base font for table */
                background-color: var(--secondary-color);
                min-width: 800px; /* Prevent excessive squishing on small screens */
            }}

            th, td {{
                padding: 15px 20px; /* Generous padding */
                text-align: left;
                vertical-align: middle;
                border-bottom: 1px solid var(--border-color);
                white-space: nowrap; /* Prevent wrapping by default */
            }}
            td {{ padding: 13px 20px; }} /* Slightly less vertical padding for data rows */

            th {{
              background-color: var(--light-gray);
              color: var(--text-color);
              font-weight: 700;
              letter-spacing: 0.02em;
              position: sticky; /* Sticky header */
              top: 0;
              z-index: 10;
              border-bottom: 2px solid var(--border-color); /* Stronger header bottom border */
              border-top: none;
              border-left: none;
              border-right: none;
            }}

            /* Sortable Header Styles */
            th.sortable {{
                cursor: pointer;
                position: relative;
                padding-right: 35px; /* More space for arrows */
                transition: background-color 0.2s ease;
            }}
            th.sortable:hover {{ background-color: var(--medium-gray); }}

            /* Sort Arrows */
            th.sortable::before,
            th.sortable::after {{
              content: "";
              position: absolute;
              right: 15px; /* Position arrows */
              opacity: 0.3; /* Dim inactive arrows */
              border: 5px solid transparent; /* Arrow size */
              transition: opacity 0.2s ease, border-color 0.2s ease;
            }}
            th.sortable::before {{ /* Up arrow */
                top: calc(50% - 11px); /* Position */
                border-bottom-color: var(--sort-indicator-inactive);
            }}
            th.sortable::after {{ /* Down arrow */
                bottom: calc(50% - 11px); /* Position */
                border-top-color: var(--sort-indicator-inactive);
            }}
            /* Active sort states */
            th.sortable.sorted-asc::before,
            th.sortable.sorted-desc::after {{
                opacity: 1; /* Full opacity for active arrow */
            }}
            th.sortable.sorted-asc::before {{ border-bottom-color: var(--sort-indicator-active); }}
            th.sortable.sorted-desc::after {{ border-top-color: var(--sort-indicator-active); }}


            /* Column Specific Styles */
            th[data-col-key="col_rank"], td:nth-child(1) {{
                text-align: center;
                min-width: 60px;
                width: 60px; /* Fixed width for rank */
            }}
            td:nth-child(1) {{ /* Rank cell */
                font-weight: 700;
                color: var(--primary-color);
                font-size: 1.05em;
            }}
            th[data-col-key="col_model"], td:nth-child(2) {{
                text-align: left;
                min-width: 300px; /* Ensure model name has space */
                white-space: normal; /* Allow model name to wrap if needed */
            }}
            th[data-col-key="col_org"], td:nth-child(3) {{
                min-width: 150px;
                white-space: normal; /* Allow org name to wrap */
            }}
            th[data-col-key="col_score"], td:nth-child(4),
            th[data-col-key="col_elo"], td:nth-child(5),
            th[data-col-key="col_tokens"], td:nth-child(6) {{
                text-align: center;
                min-width: 110px;
            }}


            /* Row Styles */
            tr {{ transition: background-color 0.15s ease-in-out; }}
            /* tr:nth-child(even) {{ background-color: var(--light-gray); }} */ /* Removed alternating color */
            tr:hover {{ background-color: #f1f3f5; }} /* Slightly darker hover than light-gray */
            tr:last-child td {{ border-bottom: none; }} /* Remove border on last row */
            tr.filtered-out {{ display: none; }} /* Hide filtered rows */

            /* Model Tag Styles */
            .model-tag {{
                padding: 3px 9px; /* Adjust padding */
                border-radius: 4px;
                font-size: 0.85em; /* Slightly larger tag text */
                white-space: nowrap;
                display: inline-block;
                vertical-align: middle;
                line-height: 1.3;
                font-weight: 700;
                border: 1px solid; /* Use border instead of just background */
                margin-left: 5px; /* Add space before tag */
            }}
            .model-judge {{
                background-color: var(--judge-bg);
                color: var(--judge-color-text);
                border-color: var(--judge-color-border);
            }}
            .model-baseline {{
                background-color: var(--baseline-bg);
                color: var(--baseline-color-text);
                border-color: var(--baseline-color-border);
            }}

            /* --- Media Queries for Responsiveness --- */
            @media (max-width: 992px) {{
                 .container {{ padding: 30px; }}
                 th, td {{ padding: 12px 15px; }}
                 th[data-col-key="col_model"], td:nth-child(2) {{ min-width: 250px; }}
            }}

            @media (max-width: 768px) {{
              .container {{ padding: 25px 20px; }}
              h1 {{ font-size: 2em; margin-bottom: 30px; }}
              body {{ padding: 20px 10px; }}
              .controls-container {{ grid-template-columns: 1fr; gap: 20px; }} /* Stack controls */
              .search-container {{ max-width: 100%; }}
              th, td {{ padding: 10px 12px; font-size: 0.9rem; }}
              th.sortable {{ padding-right: 30px; }}
              th.sortable::before, th.sortable::after {{ right: 10px; border-width: 4px; }}
              th.sortable::before {{ top: calc(50% - 9px); }}
              th.sortable::after {{ bottom: calc(50% - 9px); }}
              th[data-col-key="col_model"], td:nth-child(2) {{ min-width: 200px; }}
              th[data-col-key="col_org"], td:nth-child(3) {{ min-width: 120px; }}
              .leaderboard-table {{ min-width: 600px; }} /* Adjust min-width */
            }}

            @media (max-width: 480px) {{
                .container {{ padding: 20px 15px; }}
                h1 {{ font-size: 1.7em; }}
                .notice {{ font-size: 0.9em; padding: 12px 15px; }}
                .leaderboard-table {{ font-size: 0.85rem; }}
                th, td {{ padding: 9px 10px; }}
                th.sortable {{ padding-right: 25px; }}
                th.sortable::before, th.sortable::after {{ right: 8px; border-width: 4px; }}
                th.sortable::before {{ top: calc(50% - 8px); }}
                th.sortable::after {{ bottom: calc(50% - 8px); }}
                .control-group label {{ font-size: 0.75em; }}
                .control-group select, .control-group input[type="text"] {{ font-size: 0.95rem; padding: 10px 12px; }}
                .control-group select {{ padding-right: 35px; background-position: right 12px center; }}
                th[data-col-key="col_model"], td:nth-child(2) {{ min-width: 160px; }}
                .model-tag {{ font-size: 0.8em; padding: 2px 6px; }}
                .leaderboard-table {{ min-width: 500px; }} /* Further adjust min-width */
            }}

          </style>
        </head>
        <body>
          <div class="container">
            <!-- Heading (Link added) -->
            <h1><a href="https://github.com/qwopqwop200/ko-arena-hard-auto" target="_blank" rel="noopener noreferrer" data-translate-key="heading"></a></h1>

            <!-- Top Controls: Leaderboard and Language -->
            <div class="controls-container">
              <div class="control-group">
                <label for="leaderboard-select" data-translate-key="select_leaderboard_label"></label>
                <select id="leaderboard-select">
                  {leaderboard_dropdown_options}
                </select>
              </div>
              <div class="control-group">
                 {language_dropdown}
              </div>
            </div>

            <!-- Notice -->
            <p class="notice" data-translate-key="notice"></p>

            <!-- Search Input -->
            <div class="search-container">
                <div class="control-group">
                    <!-- Label removed, input only -->
                    {search_input_html}
                </div>
            </div>

            <!-- Table Containers -->
            {table_containers}

          </div>

          {scripts_section}
        </body>
        </html>
        """

        # --- JavaScript Section ---
        # (Keep the scripts_section_html string as is)
        scripts_section_html = f"""
          <script>
            // --- Configuration ---
            var translationsData = {translations_json};
            var updateDate = "{update_date}";
            var defaultLang = "{default_lang}";
            var currentSort = {{ key: 'col_rank', dir: 'desc' }}; // Default sort: Rank descending

            // --- DOM Elements ---
            var leaderboardSelect = document.getElementById('leaderboard-select');
            var languageSelect = document.getElementById('language-select');
            var searchInput = document.getElementById('model-search-input');
            var tableContainerParent = document.querySelector('.container'); // Or specific parent if needed
            var translatableElements; // Will be populated on DOMContentLoaded

            // --- Core Functions ---

            /**
             * Gets the currently visible table element.
             * @returns {{HTMLTableElement | null}} The visible table or null.
             */
            function getVisibleTable() {{
              var visibleContainer = document.querySelector('.table-container[style*="display: block"]');
              return visibleContainer ? visibleContainer.querySelector('table.leaderboard-table') : null;
            }}

            /**
             * Updates text content and placeholders based on the selected language.
             * @param {{string}} lang - The language code (e.g., 'ko', 'en').
             */
            function updateTranslations(lang) {{
              document.documentElement.lang = lang; // Update html lang attribute

              translatableElements.forEach(function(el) {{
                var key = el.dataset.translateKey;
                var placeholderKey = el.dataset.translateKeyPlaceholder;
                var translatedText = '';
                var isPlaceholder = false;

                if (placeholderKey) {{
                  key = placeholderKey;
                  isPlaceholder = true;
                }}

                // Get translation, fallback to defaultLang, then key itself
                if (translationsData[lang] && translationsData[lang][key]) {{
                  translatedText = translationsData[lang][key];
                }} else if (translationsData[defaultLang] && translationsData[defaultLang][key]) {{
                  console.warn('Missing translation for key: ' + key + ' in language: ' + lang + '. Falling back.');
                  translatedText = translationsData[defaultLang][key];
                }} else {{
                  console.error('Missing translation for key: ' + key + '.');
                  translatedText = key; // Use key as fallback text
                }}

                // Replace dynamic values like update_date - Use double braces {{{{}}}} for literal braces
                translatedText = translatedText.replace('{{{{update_date}}}}', updateDate); // Correctly escape for JS replace inside f-string

                // Update element content or attribute
                if (isPlaceholder) {{
                  el.placeholder = translatedText;
                }} else if (el.tagName === 'TITLE') {{
                  el.textContent = translatedText;
                }} else {{
                  // Use innerHTML for elements that might contain HTML tags (like the notice)
                  // Use textContent for others (like labels, options, headers) for security and performance
                  if (key === 'notice') {{
                     el.innerHTML = translatedText;
                  }} else {{
                     el.textContent = translatedText;
                  }}
                }}
              }});

              // Update table headers specifically (since they are generated dynamically)
              var visibleTable = getVisibleTable();
              if (visibleTable) {{
                var headers = visibleTable.querySelectorAll('thead th[data-col-key]');
                headers.forEach(function(th) {{
                  var key = th.dataset.colKey;
                  var headerText = key; // Fallback
                  if (translationsData[lang] && translationsData[lang][key]) {{
                    headerText = translationsData[lang][key];
                  }} else if (translationsData[defaultLang] && translationsData[defaultLang][key]) {{
                    headerText = translationsData[defaultLang][key];
                  }}
                  th.textContent = headerText; // Update header text
                }});
                // Re-apply sort indicators after text change
                updateSortIndicators(visibleTable);
              }}
            }}

            /**
             * Filters table rows based on the search input value.
             */
            function filterTable() {{
                var searchTerm = searchInput.value.toLowerCase().trim();
                var visibleTable = getVisibleTable();
                if (!visibleTable) return;

                var rows = visibleTable.querySelectorAll('tbody tr');
                rows.forEach(function(row) {{
                    var modelName = row.dataset.modelName || ''; // Get model name from data attribute
                    var isMatch = modelName.includes(searchTerm);
                    row.classList.toggle('filtered-out', !isMatch); // Add/remove class to hide/show
                }});
            }}

            /**
             * Updates the visual indicators (arrows) on sortable table headers.
             * @param {{HTMLTableElement}} table - The table to update indicators for.
             */
            function updateSortIndicators(table) {{
                if (!table) table = getVisibleTable();
                if (!table) return;

                var headers = table.querySelectorAll('thead th.sortable');
                headers.forEach(function(th) {{
                    th.classList.remove('sorted-asc', 'sorted-desc');
                    if (th.dataset.colKey === currentSort.key) {{
                        th.classList.add(currentSort.dir === 'asc' ? 'sorted-asc' : 'sorted-desc');
                    }}
                }});
            }}

            /**
             * Sorts the table rows based on a column key and type.
             * @param {{string}} key - The data-col-key of the header clicked.
             * @param {{string}} type - The sort type ('numeric' or 'text').
             * @param {{HTMLTableElement}} table - The table to sort.
             */
            function sortTable(key, type, table) {{
                if (!table) table = getVisibleTable();
                if (!table) return;
                var tbody = table.querySelector('tbody');
                if (!tbody) return;

                var rows = Array.from(tbody.querySelectorAll('tr'));

                // Determine sort direction
                var newDir = 'asc';
                if (currentSort.key === key) {{
                    newDir = currentSort.dir === 'asc' ? 'desc' : 'asc';
                }} else {{
                    // Default direction for new column sort
                    // Rank: descending, Score: descending, Elo: descending, Tokens: ascending, Others: ascending
                    newDir = (key === 'col_rank' || key === 'col_score' || key === 'col_elo') ? 'desc' : 'asc';
                }}

                // Find the index of the column based on the key
                var headerIndex = getHeaderIndex(table, key);
                if (headerIndex === -1) {{
                    // Use template literal safely within JS
                    console.error(`Sort Error: Column key "${{key}}" not found in table headers.`);
                    return;
                }}
                var cellIndex = headerIndex; // 0-based index for querySelectorAll

                rows.sort(function(rowA, rowB) {{
                    // Get the cell using the determined index
                    var cellA = rowA.querySelectorAll('td')[cellIndex];
                    var cellB = rowB.querySelectorAll('td')[cellIndex];

                    if (!cellA || !cellB) {{
                        // Use template literal safely within JS
                        console.warn(`Sort Warning: Cell not found at index ${{cellIndex}} for key "${{key}}".`);
                        return 0;
                    }}

                    // Get sort values from data-sort-value attribute
                    var valA = cellA.dataset.sortValue;
                    var valB = cellB.dataset.sortValue;
                    var comparison = 0;

                    if (type === 'numeric') {{
                        var numA = parseFloat(valA);
                        var numB = parseFloat(valB);
                        // Handle NaN values (treat them as lowest or highest depending on sort direction)
                        numA = isNaN(numA) ? (newDir === 'asc' ? Infinity : -Infinity) : numA;
                        numB = isNaN(numB) ? (newDir === 'asc' ? Infinity : -Infinity) : numB;
                        comparison = numA - numB;
                    }} else {{ // 'text' sort
                        valA = String(valA).toLowerCase();
                        valB = String(valB).toLowerCase();
                        comparison = valA.localeCompare(valB);
                    }}

                    // Apply direction
                    return newDir === 'asc' ? comparison : -comparison;
                }});

                // Re-append rows in sorted order
                rows.forEach(row => tbody.appendChild(row));

                // Update current sort state
                currentSort = {{ key: key, dir: newDir }};
                updateSortIndicators(table);
            }}

            /**
             * Gets the 0-based index of a header column by its key.
             * @param {{HTMLTableElement}} table - The table element.
             * @param {{string}} key - The data-col-key to find.
             * @returns {{number}} The index or -1 if not found.
             */
            function getHeaderIndex(table, key) {{
                var headers = table.querySelectorAll('thead th');
                for (var i = 0; i < headers.length; i++) {{
                    if (headers[i].dataset.colKey === key) {{
                        return i;
                    }}
                }}
                return -1; // Not found
            }}

            /**
             * Gets the sort type ('numeric' or 'text') for a given column key.
             * @param {{HTMLTableElement}} table - The table element.
             * @param {{string}} key - The data-col-key.
             * @returns {{string}} The sort type ('numeric' or 'text').
             */
            function getHeaderSortType(table, key) {{
                if (!table || !key) return 'text';
                // Use template literal safely within JS
                var header = table.querySelector(`th[data-col-key="${{key}}"]`);
                return header ? (header.dataset.sortType || 'text') : 'text';
            }}


            // --- Event Listeners ---

            // Leaderboard selection change
            leaderboardSelect.addEventListener('change', function() {{
              var selectedId = this.value;
              var targetTableId = 'table-' + selectedId;
              var allContainers = document.querySelectorAll('.table-container');

              allContainers.forEach(function(container) {{
                container.style.display = (container.id === targetTableId) ? 'block' : 'none';
              }});

              // Reset sort to default (Rank Desc) when changing tables
              currentSort = {{ key: 'col_rank', dir: 'desc' }};
              var newVisibleTable = getVisibleTable();
              if (newVisibleTable) {{
                 // Apply default sort to the newly visible table
                 sortTable(currentSort.key, getHeaderSortType(newVisibleTable, currentSort.key), newVisibleTable);
                 // Update headers and indicators for the new table
                 updateTranslations(languageSelect.value); // Ensure headers are translated
              }}
              filterTable(); // Re-apply filter
            }});

            // Language selection change
            languageSelect.addEventListener('change', function() {{
              var selectedLang = this.value;
              updateTranslations(selectedLang);
              // No need to update placeholder separately, updateTranslations handles it
            }});

            // Search input typing
            searchInput.addEventListener('input', filterTable);

            // Table header clicks for sorting (using event delegation)
            tableContainerParent.addEventListener('click', function(event) {{
                // Find the closest sortable header that was clicked
                var header = event.target.closest('th.sortable');
                // Ensure the click was on a header within the currently visible table
                var visibleTable = getVisibleTable();
                if (header && visibleTable && visibleTable.contains(header)) {{
                    var key = header.dataset.colKey;
                    var type = getHeaderSortType(visibleTable, key);
                    sortTable(key, type, visibleTable);
                }}
            }});

            // --- Initialization ---
            document.addEventListener('DOMContentLoaded', function() {{
                // Query all elements needing translation *after* DOM is ready
                translatableElements = document.querySelectorAll('[data-translate-key], [data-translate-key-placeholder]');
                // Initial translation update
                updateTranslations(languageSelect.value);

                // Apply initial sort to the default visible table
                var initialTable = getVisibleTable();
                if (initialTable) {{
                    // currentSort is already set to default {{{{ key: 'col_rank', dir: 'desc' }}}}
                    sortTable(currentSort.key, getHeaderSortType(initialTable, currentSort.key), initialTable);
                }}
                // Apply initial filter (if any search term is pre-filled, though unlikely here)
                filterTable();
            }});
          </script>
          """

        # --- Generate Final HTML ---
        # (Keep this section as is)
        final_html = html_template.format(
            default_lang=default_lang,
            update_date=update_date,
            leaderboard_dropdown_options=leaderboard_dropdown_options_html,
            language_dropdown=language_dropdown_html,
            search_input_html=search_input_html,
            table_containers=table_containers_html,
            scripts_section=scripts_section_html # Inject the JavaScript block
        )

        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Leaderboard HTML successfully generated with medal emojis at: {output_html_path}")

    except FileNotFoundError as e: print(f"Error: {e}")
    except ValueError as e: print(f"Error: {e}")
    except Exception as e: print(f"An unexpected error occurred: {e}"); import traceback; traceback.print_exc()