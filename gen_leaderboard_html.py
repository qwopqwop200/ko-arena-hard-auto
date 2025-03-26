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
                print(f"Skipping file with unexpected date format: {filename}")
                continue

            if latest_date is None or file_date > latest_date:
                latest_date = file_date
                latest_file = filename

    if latest_file is None:
        raise FileNotFoundError(f"No leaderboard CSV file found in {directory} with pattern '{base}YYYYMMDD{suffix}'")
    return os.path.join(directory, latest_file)


def deploy_leaderboard(csv_path: str, html_path: str) -> None:
    df = pd.read_csv(csv_path)
    df = df.sort_values(by='score', ascending=False)

    model_map = {
        'claude-3.7-sonnet': 'claude-3.7-sonnet (baseline)',
        'gemini-2.0-flash-001': 'gemini-2.0-flash-001 (judge)',
        'gpt-4o-mini': 'gpt-4o-mini (judge)'
    }
    df['model'] = df['model'].replace(model_map)

    def style_model(model: str) -> str:
        if "(judge)" in model:
            return f'<span class="model-tag model-judge">{model}</span>'
        elif "(baseline)" in model:
            return f'<span class="model-tag model-baseline">{model}</span>'
        else:
            return model
    df['model'] = df['model'].apply(style_model)

    df['avg_tokens'] = df['avg_tokens'].astype(int)
    df['CI'] = df['CI'].fillna('')
    df['score'] = df['score'].round(2).astype(str) + df['CI']

    try:
        update_date_dt = pd.to_datetime(df['date'].iloc[0])
        update_date = update_date_dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError, IndexError):
        update_date = datetime.now().strftime("%Y-%m-%d")
        print(f"Warning: Could not parse date from CSV, using current date: {update_date}")

    df = df[['model', 'score', 'avg_tokens']]

    df = df.reset_index(drop=True)
    df.index += 1
    df.insert(0, 'Rank', df.index)

    df.rename(columns={
        'model': 'Model',
        'score': 'Score (CI)',
        'avg_tokens': 'Avg. Tokens',
    }, inplace=True)

    html_template = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Ko-Arena-Hard Leaderboard ({update_date})</title>
      <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
      <style>
        :root {{
          --primary-color: #008080;
          --secondary-color: #ffffff;
          --accent-color: #FFD700;
          --text-color: #333;
          --light-gray: #f8f9fa;
          --medium-gray: #e9ecef;
          --dark-gray: #6c757d;
          --judge-color: #dc3545;
          --judge-bg: #f8d7da;
          --baseline-color: #007bff;
          --baseline-bg: #cfe2ff;
          --border-radius: 8px;
          --box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }}

        body {{
          font-family: 'Noto Sans KR', 'Roboto', sans-serif;
          background: linear-gradient(135deg, #e0f2f1, #ffffff);
          margin: 0;
          padding: 30px 15px;
          color: var(--text-color);
          line-height: 1.6;
        }}

        .container {{
          max-width: 1100px;
          margin: 30px auto;
          background: var(--secondary-color);
          padding: 30px 40px;
          border-radius: var(--border-radius);
          box-shadow: var(--box-shadow);
        }}

        h1 {{
          text-align: center;
          margin-bottom: 25px;
          color: var(--primary-color);
          font-weight: 700;
        }}
        h1 a {{
             color: inherit;
             text-decoration: none;
             transition: color 0.3s ease;
        }}
        h1 a:hover {{
            color: #005a5a;
        }}

        .notice {{
          background-color: var(--judge-bg);
          color: var(--judge-color);
          border-left: 5px solid var(--judge-color);
          padding: 15px 20px;
          margin-bottom: 30px;
          border-radius: 4px;
          font-size: 0.95em;
        }}
        .notice strong {{
            color: var(--judge-color);
        }}

        .table-container {{
          overflow-x: auto;
          -webkit-overflow-scrolling: touch;
        }}

        .leaderboard-table {{
          width: 100%;
          border-collapse: collapse;
          margin-top: 20px;
          font-size: 0.95em;
        }}

        th, td {{
          padding: 14px 18px;
          text-align: left;
          vertical-align: middle;
          border-bottom: 1px solid var(--medium-gray);
        }}

        th {{
          background-color: var(--primary-color);
          color: var(--secondary-color);
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          white-space: nowrap;
        }}

        th:first-child, td:first-child {{
          text-align: center;
          min-width: 50px;
        }}
        td:first-child {{
          font-weight: 700;
          color: var(--primary-color);
          font-size: 1.1em;
        }}

         th:nth-child(3),
         th:nth-child(4),
         th:nth-child(5) {{
             text-align: center;
         }}
         td:nth-child(3),
         td:nth-child(4),
         td:nth-child(5) {{
             text-align: center;
             white-space: nowrap;
         }}

        tr {{
          transition: background-color 0.2s ease-in-out;
        }}

        tr:nth-child(even) {{
          background-color: var(--light-gray);
        }}

        tr:hover {{
          background-color: var(--medium-gray);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        .model-tag {{
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.9em;
            white-space: nowrap;
        }}
        .model-judge {{
            background-color: var(--judge-bg);
            color: var(--judge-color);
            border: 1px solid var(--judge-color);
            font-weight: 700;
        }}
        .model-baseline {{
            background-color: var(--baseline-bg);
            color: var(--baseline-color);
            border: 1px solid var(--baseline-color);
            font-weight: 700;
        }}

        @media (max-width: 768px) {{
          .container {{
            padding: 20px;
          }}
          th, td {{
            padding: 10px 12px;
          }}
          h1 {{
            font-size: 1.8em;
          }}
          body {{
             padding: 20px 10px;
          }}
        }}

        @media (max-width: 480px) {{
            h1 {{
                font-size: 1.5em;
            }}
            .notice {{
                font-size: 0.9em;
                padding: 10px 15px;
            }}
             .leaderboard-table {{
                 font-size: 0.85em;
             }}
              th, td {{
                padding: 8px 10px;
              }}
        }}

      </style>
    </head>
    <body>
      <div class="container">
        <h1><a href="https://github.com/qwopqwop200/ko-arena-hard-auto" target="_blank" rel="noopener noreferrer">Ko-Arena-Hard-Auto Leaderboard ({update_date})</a></h1>

        <p class="notice">
          <strong style="color: var(--judge-color)">주의:</strong> judge 모델(gemini-2.0-flash, gpt-4o-mini)은 자체 답변 선호 경향으로 인해 실제 성능보다 점수가 높게 나타날 수 있습니다. 해당 모델들의 점수 해석 시 유의하시기 바랍니다.
        </p>

        <div class="table-container">
          {table}
        </div>
      </div>
    </body>
    </html>
    """

    table_html = df.to_html(classes="leaderboard-table", border=0, escape=False, index=False)

    final_html = html_template.format(table=table_html, update_date=update_date)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Leaderboard HTML successfully generated at: {html_path}")

if __name__ == '__main__':
    try:
        leaderboard_dir = './leaderboard/'
        csv_file = get_latest_leaderboard_csv(leaderboard_dir)
        print(f"Using latest leaderboard CSV: {csv_file}")

        output_dir = 'dist'
        os.makedirs(output_dir, exist_ok=True)

        output_html = os.path.join(output_dir, 'leaderboard.html')

        deploy_leaderboard(csv_file, output_html)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")