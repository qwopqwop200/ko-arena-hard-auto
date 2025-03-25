import os
import pandas as pd
from datetime import datetime

def get_latest_leaderboard_csv(directory: str) -> str:
    base = "arena_hard_leaderboard_"
    suffix = "_ensemble.csv"
    latest_date = None
    latest_file = None

    for filename in os.listdir(directory):
        if filename.startswith(base) and filename.endswith(suffix):
            date_str = filename[len(base):-len(suffix)]
            try:
                file_date = datetime.strptime(date_str, "%Y%m%d")
            except ValueError:
                continue
            if latest_date is None or file_date > latest_date:
                latest_date = file_date
                latest_file = filename

    if latest_file is None:
        raise FileNotFoundError(f"No leaderboard CSV file found in {directory}")
    return os.path.join(directory, latest_file)

def deploy_leaderboard(csv_path: str, html_path: str) -> None:
    df = pd.read_csv(csv_path)
    df = df.sort_values(by='score', ascending=False)
    df['model'] = df['model'].replace('claude-3.7-sonnet', 'claude-3.7-sonnet (baseline)')
    df['model'] = df['model'].replace('gemini-2.0-flash-001', 'gemini-2.0-flash-001 (judge)')
    df['model'] = df['model'].replace('gpt-4o-mini', 'gpt-4o-mini (judge)')

    def style_model(model: str) -> str:
        if "(judge)" in model:
            return f'<strong style="color: darkred">{model}</strong>'
        elif "(baseline)" in model:
            return f'<strong>{model}</strong>'
        else:
            return model
    df['model'] = df['model'].apply(style_model)

    df['avg_tokens'] = df['avg_tokens'].astype(int)
    df['score'] = df['score'].astype(str) + df['CI']
    update_date = df['date'].iloc[0]
    df = df.drop(columns=['rating_q025', 'rating_q975', 'CI', 'date'], errors='ignore')

    html_template = """
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Leaderboard (Update {update_date})</title>
      <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">
      <style>
        :root {{
          --primary-color: #4CAF50;
          --secondary-color: #fff;
          --bg-gradient-start: #f0f0f0;
          --bg-gradient-end: #ffffff;
          --text-color: #333;
        }}
        body {{
          font-family: 'Roboto', sans-serif;
          background: linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end));
          margin: 0;
          padding: 40px;
          color: var(--text-color);
        }}
        .container {{
          max-width: 1000px;
          margin: 0 auto;
          background: #fff;
          padding: 20px 30px;
          border-radius: 8px;
          box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
          text-align: center;
          margin-bottom: 20px;
        }}
        .table-container {{
          overflow-x: auto;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
          margin-top: 20px;
        }}
        th, td {{
          padding: 15px;
          text-align: center;
        }}
        th {{
          background-color: var(--primary-color);
          color: var(--secondary-color);
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }}
        tr {{
          border-bottom: 1px solid #e0e0e0;
          transition: background-color 0.3s ease;
        }}
        tr:nth-child(even) {{
          background-color: #fafafa;
        }}
        tr:hover {{
          background-color: #f1f1f1;
        }}
        @media (max-width: 600px) {{
          th, td {{
            padding: 10px;
          }}
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1><a href="https://github.com/qwopqwop200/ko-arena-hard-auto" target="_blank">Ko-Arena-Hard-Auto Leaderboard (Update {update_date})</a></h1>
        <p class="notice"><strong style="color: darkred">judge 모델(gemini-2.0-flash, gpt-4o-mini)들은 자기 답변을 선호하는 경향있으며 실제보다 더 높은 점수를 받았을 가능성이 있습니다.<br> 때문에 judge 모델들은 해석에 주의가 필요합니다.</strong></p>
        <div class="table-container">
          {table}
        </div>
      </div>
    </body>
    </html>
    """
    df = df.reset_index(drop=True)
    df.index += 1
    table_html = df.to_html(index=True, border=0, justify='center', escape=False)
    final_html = html_template.format(table=table_html, update_date=update_date)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == '__main__':
    csv_file = get_latest_leaderboard_csv('./leaderboard/')
    os.makedirs('dist', exist_ok=True)
    output_html = 'dist/leaderboard.html'
    deploy_leaderboard(csv_file, output_html)