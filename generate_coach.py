name: Daily Business English Coach

on:
  schedule:
    # 每天北京时间早上 8:30 运行 (UTC 时间 00:30)
    - cron: '30 0 * * *'
  workflow_dispatch: # 允许手动触发

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install google-generativeai markdown

    # 1. 运行脚本并将 AI 生成的教案保存到 output.md
    - name: Run Coach Script
      env:
        AI_API_KEY: ${{ secrets.AI_API_KEY }}
      run: |
        python generate_coach.py > output.md
        cat output.md

    # 2. 用极其简单安全的方式，把 Markdown 转换成干净好看的 HTML 网页邮件
    - name: Convert Markdown to Beautiful HTML
      run: |
        python -c "
        import markdown
        with open('output.md', 'r', encoding='utf-8') as f:
            text = f.read()
        html_content = markdown.markdown(text, extensions=['extra', 'codehilite'])
        
        # 纯静态精美样式，绝对没有任何复杂的 JS 脚本和符号冲突
        styled_html = f'''
        <html>
        <head>
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.7; color: #333333; max-width: 650px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #1a73e8; border-bottom: 2px solid #e8eaed; padding-bottom: 8px; font-size: 24px; }}
            h2 {{ color: #202124; font-size: 20px; margin-top: 24px; border-left: 4px solid #1a73e8; padding-left: 10px; }}
            h3 {{ color: #5f6368; font-size: 16px; }}
            p, li {{ font-size: 15px; color: #3c4043; }}
            code {{ background-color: #f1f3f4; color: #b06000; padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', Courier, monospace; font-size: 14px; }}
            blockquote {{ background-color: #f8f9fa; border-left: 4px solid #f4b400; margin: 1.5em 0; padding: 12px 20px; font-style: italic; border-radius: 0 8px 8px 0; }}
            ul, ol {{ padding-left: 20px; }}
            li {{ margin-bottom: 8px; }}
            strong {{ color: #000000; background-color: #fff9c4; padding: 0 2px; }}
            .footer {{ margin-top: 40px; padding-top: 15px; border-top: 1px solid #e8eaed; font-size: 12px; color: #aaabad; text-align: center; }}
          </style>
        </head>
        <body>
          {html_content}
          <div class='footer'>🤖 本教案由 AI 英语教练全自动生成派送</div>
        </body>
        </html>
        '''
        with open('beautiful_output.html', 'w', encoding='utf-8') as f:
            f.write(styled_html)
        "

    # 3. 自动通过 Gmail 发送排版完美的 HTML 邮件
    - name: Send Mail
      uses: dawidd6/action-send-mail@v3
      with:
        server_address: smtp.gmail.com
        server_port: 465
        
        username: siaoutta@gmail.com
        password: ${{ secrets.EMAIL_GITHUB }}
        
        subject: 🚀 今日商务英语每日课 (Daily English Coach)
        from: AI Coach <siaoutta@gmail.com>
        
        to: siaoutta@gmail.com,267247961@qq.com,caisihao@asp.th.com
        html_body: file://beautiful_output.html
