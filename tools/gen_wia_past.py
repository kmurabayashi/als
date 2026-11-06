"""WIA の過去イベントページ(site/wia/<slug>/index.html)を生成する。

内容は wiajapan.org の各ページ(reference/wia-past/*.html)と CodeZine の記事から起こしたもの。
直すときはこのファイルを編集して `python3 tools/gen_wia_past.py` を実行する。
"""
import os

ROOT = os.path.join(os.path.dirname(__file__), '..', 'site', 'wia')
ALS = 'https://als-2027-b95.pages.dev/'
FONTS = 'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Inter:wght@600;800&family=Raleway:wght@300;400;500;600&display=swap'
PAST = [
    ('/2026/', 'Women in Agile Tokyo 2026', '2026.02.03–04'),
    ('/osaka-2025/', 'Women in Agile Osaka 2025', '2025.09.13'),
    ('/2025/', 'Women in Agile Tokyo 2025', '2025.02.04–05'),
    ('/2024/', 'Women in Agile Tokyo 2024', '2024.02.06'),
]


def page(cur, title, desc, eyebrow, lead, facts, body, year):
    li = ''.join(
        f'\n            <li><a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}<small>{d}</small></a></li>'
        for h, t, d in PAST)
    fx = ''.join(f'\n          <div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in facts)
    h1 = title.replace('Women in Agile ', 'Women in Agile<br>')
    return f'''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="/style.css">
  <link rel="stylesheet" href="/als.css">
  <script src="/nav.js" defer></script>
</head>
<body class="theme-als theme-wia">
  <header class="nav">
    <div class="wrap nav-inner">
      <a href="/" class="logo">WIA <span>Tokyo 2027</span></a>
      <nav class="gnav">
          <details class="dropdown">
            <summary>過去イベント</summary>
            <ul>{li}
            </ul>
          </details>
          <a class="nav-anchor" href="{ALS}">Agile Leadership Summit 2027</a>
      </nav>
    </div>
  </header>
  <div class="archive-bar">このページは過去のイベントです。最新情報は <a href="/">Women in Agile Tokyo 2027</a> へ</div>

  <main>
    <section class="hero">
      <div class="wrap">
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        <dl class="facts">{fx}
        </dl>
      </div>
    </section>
{body}
  </main>

  <footer class="footer">
    <div class="wrap">
      <p>最新:<a href="/">Women in Agile Tokyo 2027</a> / <a href="{ALS}">Agile Leadership Summit 2027</a></p>
      <p>© {year} Women in Agile Japan</p>
    </div>
  </footer>
</body>
</html>
'''


def sec(label, ja, inner, alt=False, center=False):
    return f'''
    <section class="section{' alt' if alt else ''}">
      <div class="wrap{' center' if center else ''}">
        <div class="section-head">
          <p class="section-label">{label}</p>
          <h2>{ja}</h2>
        </div>
{inner}
      </div>
    </section>'''


def tl(items):
    out = ''.join(f'\n              <li><time>{t}</time><span><span class="tl-label">{lab}</span>{txt}</span></li>'
                  for t, lab, txt in items)
    return f'            <ol class="timeline">{out}\n            </ol>'


def speakers(sp):
    out = ''
    for s in sp:
        img = f'\n            <img src="/images/{s["img"]}" alt="{s["name"]}" loading="lazy">' if s.get('img') else ''
        org = f'\n            <p class="speaker-org">{s["org"]}</p>' if s.get('org') else ''
        tt = f'\n            <p class="talk-title">「{s["title"]}」</p>' if s.get('title') else ''
        bios = ''.join(f'\n            <p class="bio">{b}</p>' for b in s['bio'])
        out += f'''
          <article>{img}
            <p class="speaker-role">{s["role"]}</p>
            <p class="speaker-name">{s["name"]}</p>{org}{tt}{bios}
          </article>'''
    return f'        <div class="speakers">{out}\n        </div>'


def logos(items):
    li = ''.join(f'\n          <li><img src="/images/logos/{f}" alt="{a}" loading="lazy"></li>' for f, a in items)
    return f'        <ul class="logos">{li}\n        </ul>'


def links(ls):
    return '        <p class="center">' + ' '.join(f'<a class="btn ghost" href="{u}">{t}</a>' for t, u in ls) + '</p>'


OST = '参加者全員が「主役」となり、自由にテーマを提案し、関心のあるトピックについて深い対話を行う新しい形式のセッションです。固定的なアジェンダや発表者を設けず、その場で生まれる「化学反応」を大切にした対話の場を創出します。'
PRINCIPLES = '''        <div class="cards">
          <div class="card"><h3>「4つの原則」を大切に</h3><p>集まった人が適切な人々である/始まった時が適切な時である/起こることは全て起こるべくして起こる/終わった時が適切な時である</p></div>
          <div class="card"><h3>「1つの法則」を実践</h3><p>「足による投票の法則」:自分が学んだり貢献したりできないと感じたら、自分から別のグループに移動する</p></div>
        </div>'''
KEYNOTE_LEAD = '        <p class="center">3つの特別なキーノートセッションを通じて、明日からの一歩を後押しする学びと勇気を、ぜひ見つけてください。</p>\n'


def two_days(hallb):
    d1 = tl([('9:15', 'Door Open', '受付開始'),
             ('10:00', 'Opening · Keynote', 'オープニング・キーノート'),
             ('13:00', 'Sessions', f'3 トラックでセッションを行います<small>Hall A:Women in Agile</small><small>Hall B:{hallb}</small><small>Room C:スポンサーセッション</small>'),
             ('18:00', 'Done', '本日のセッションはここまでです')])
    d2 = tl([('9:15', 'Door Open', '受付開始'),
             ('10:00', 'Open Space Technology', OST + '<small>10:00-11:00 セッション提案、タイムテーブル構成 / 11:00- セッション1 / 12:00- セッション2 + ランチタイム / 13:00- セッション3 / 14:00- セッション4 / 15:00- セッション5</small>'),
             ('16:00', 'Closing Keynote', 'クロージングキーノート'),
             ('18:00', 'Done', '本日のセッションはここまでです')])
    return f'''        <div class="days">
          <div>
            <p class="day-title">Day 1</p>
{d1}
          </div>
          <div>
            <p class="day-title">Day 2</p>
{d2}
          </div>
        </div>
{PRINCIPLES}'''


def write(slug, html):
    d = os.path.join(ROOT, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


# ---------- Tokyo 2026 ----------
body = sec('Schedule', 'スケジュール', two_days(f'<a href="{ALS}">Agile Leadership Summit</a>'))
body += sec('Keynote', 'キーノート', KEYNOTE_LEAD + speakers([
    dict(img='wia2026-takahashi.jpg', role='Women in Agile Keynote', name='高橋 真寿美 氏',
         org='STORES 株式会社 PX部門 HR本部 シニアマネジャー/ダイバーシティプロジェクトリーダー',
         bio=['株式会社リクルートマネジメントソリューションズに新卒入社。大手企業向け人材開発やコンサルティングに従事。在籍中に、経済産業省に出向。スタートアップ支援政策に関わる。株式会社ABEJAの人事を経て、2021年8月にヘイ株式会社(現:STORES 株式会社)に入社。主に人事企画・組織開発を担当する。2023年にダイバーシティプロジェクトを立ち上げる。']),
    dict(img='wia2026-seki.jpg', role='Agile Leadership Summit Keynote', name='関 将俊 氏',
         bio=['2001年からXPを実践。エクストリームなチームと25年間を過ごす。RubyKaigi2006-2024、RubyConf2013、RubyWorld Conference2023-2025スピーカー。主な著作は『The dRuby Book』、『プログラマが知るべき97のこと』(日本語版エッセイ)。']),
    dict(img='wia2026-iwakiri.jpg', role='Closing Keynote', name='岩切 晃子 氏',
         bio=['「Developers Summit(通称:デブサミ)」初代オーガナイザー(2003-2014)。異種の技術領域に携わるエンジニアが一堂に会することのできる、中立かつオープンで多様なイベントの開催を支えたことにより、楽天テクノロジーアワード2012 ルビィ賞を、自宅の倉庫に置いたライブラリの運営に対し、本を通じた人と人とのつながりを生み出し、地域に貢献する活動として、大阪府立大からマイクロライブラリーアワード2018を受賞。',
              '実践者が選んだ「スクラムマスターが読むべき60冊」を貸し出す「旅するAgile本箱」プロジェクトを2019年1月より実施中。2022年7月に独立し、現在、株式会社翔泳社顧問、クリエーションライン株式会社デベロッパーリレーションズ、株式会社フルストリームソリューションズ アドバイザー、2025年よりチームみらいサポーター。本、IT、コミュニティで社会をブーストする人を増やすために、日夜行脚中。']),
]), alt=True)
body += sec('Links', '関連リンク', links([
    ('タイムテーブル(ConfEngine)', 'https://confengine.com/conferences/women-in-agile-tokyo-2026/schedule'),
    ('開催趣意書', 'https://docs.google.com/presentation/d/11IyFoYm2IaJ9TBNDCmh8xlIsiuZpUzMQn9xg-cjtn18/edit?usp=sharing')]), center=True)
write('2026', page('/2026/', 'Women in Agile Tokyo 2026',
                   '2026年2月3日〜4日に大崎ブライトコアホールで開催した Women in Agile Tokyo 2026。',
                   'with Agile Leadership Summit', '2026年2月3日(火)〜4日(水)',
                   [('Venue', '大崎ブライトコアホール'), ('Day 1', 'キーノート + 3 トラック'), ('Day 2', 'オープンスペース')],
                   body, 2026))

# ---------- Osaka 2025 ----------
body = sec('Schedule', 'スケジュール', tl([
    ('9:15', 'Door Open', '開場'),
    ('10:00', 'Open Space Technology', OST + '<small>10:00-10:15 オープニング / 10:15-11:00 OSTの説明・テーマ募集 / 11:00- セッション1 / 12:00- ランチ / 13:00- セッション2 / 14:00- セッション3 / 15:00- セッション4</small>'),
    ('16:00', 'Closing Keynote', 'クロージングキーノート'),
    ('18:00', 'Done', '本日のセッションはここまでです')]) + '\n' + PRINCIPLES)
body += sec('Keynote', 'クロージングキーノート', speakers([
    dict(img='wia2025osaka-nabeshima.webp', role='Closing Keynote', name='鍋島 英莉 氏(なべしま えり)',
         org='翔泳社 CodeZine編集部',
         title='開発者ではない編集者の私が実践する、「良いテックカンファレンスづくり」の暗黙知',
         bio=['ITエンジニアではない編集者の私が、普段どのようなことを大事にして、デブサミ関西のようなテックカンファレンスをつくっているのかを紹介します。私自身が過去主催したカンファレンスの企画・運営で何を意識してやってきたか、そこから何を学んだのか、そもそも「良いカンファレンス」とは何なのかなどについてお話します。',
              '奈良県出身。2019年から翔泳社にて、ソフトウェア開発者向けWebメディア「CodeZine」の編集・企画・運営に携わる。2020年～2023年:若手ITエンジニア向けイベント「Developers Boost」主催。2022年〜:エンジニアのキャリアを考えるカンファレンス「Developers CAREER Boost」オーガナイザー。2024年〜:「Developers Summit KANSAI(デブサミ関西)」オーガナイザー。']),
]), alt=True)
body += sec('Links', '関連リンク', links([
    ('開催趣意書', 'https://docs.google.com/presentation/d/16pq663HQgrc4DHosCpvVhZCDn0ZvmZdc739ISapb_Yk/edit?usp=sharing')]), center=True)
write('osaka-2025', page('/osaka-2025/', 'Women in Agile Osaka 2025',
                         '2025年9月13日に開催した Women in Agile Osaka 2025。オープンスペース形式の 1 日。',
                         'Open Space Technology', '2025年9月13日(土)',
                         [('Format', 'オープンスペース'), ('Place', '大阪')], body, 2025))

# ---------- Tokyo 2025 ----------
body = sec('Schedule', 'スケジュール', two_days('運営 in Agile'))
body += sec('Keynote', 'キーノート', KEYNOTE_LEAD + speakers([
    dict(img='wia2025-janelee.jpg', role='Women in Agile Keynote', name="Jane Lee Hundley O'Connell 氏",
         org='Federal Reserve Bank of Richmond / Audit Solutions and Innovation / Project Manager',
         bio=["With over 30 years at the Federal Reserve Bank, Jane Lee has extensive experience in project management, financial and software development governance, risk, and control assessments, and leading quality assurance evaluations. Currently, she is part of the technology and data analytics team that supports the Federal Reserve System Audit Community to deliver innovations and data driven insights to stakeholders.",
              "Throughout her career, she has taken various professional and personal risks for organization’s needs and balancing personal growth. Jane Lee transitioned from financial roles to technical positions, and leading an agile transition.",
              '(Keynote では同時翻訳がつきます)']),
    dict(img='wia2025-kobase.webp', role='運営 in Agile Keynote', name='こばせ 氏(@kobase555)',
         org='ウイングアーク1st株式会社',
         bio=['これまで、XP祭り、1on1カンファレンス、スクラムフェス新潟などのカンファレンス運営に実行委員として関わる。Regional Scrum Gathering Tokyoや各地のスクラムフェスでの当日スタッフ経験もある。最近では、渋谷アジャイルのコミュニティ運営にも関わりながら、コミュニティ活動を楽しんでいる。アジャイルやスクラムの元に集まる人たちの集まりが好き(仮)。']),
    dict(img='wia2025-damuha.jpg', role='Closing Keynote', name='咸 多栄 氏(だむは)',
         org='bgrass 創業者/WAKE Career 運営',
         bio=['ジェンダーギャップをテクノロジーで解決する、女性ITエンジニア向けハイスキル転職サービス「WAKE Career」を運営。韓国生まれ日本育ち。新卒からエンジニアとして開発に従事、その傍ら女性エンジニア向け1on1サービスを個人開発。IT業界のジェンダーギャップ解消を目指し、2022年7月にbgrassを創業。2024年 Forbes Women In Tech 30 に選出。「BEYOND MILLENNIALS 2024」選出。2022年女性リーダー支援基金採択。']),
]), alt=True)
body += sec('Sponsors and Communities', 'Working Together', logos([
    ('productpeople.png', 'ProductPeople'), ('ishiifood.png', '石井食品'), ('slalom.png', 'Slalom'),
    ('takeda.png', 'Takeda'), ('stores.png', 'STORES'), ('tokyodev.png', 'TokyoDev')]))
body += sec('Links', '関連リンク', links([
    ('タイムテーブル(ConfEngine)', 'https://confengine.com/conferences/women-in-agile-tokyo-2025/schedule'),
    ('開催趣意書', 'https://docs.google.com/presentation/d/1cYsGZG5C_tmQQNqDkWjZGrwSOPOfzqbFl2PF0NryL5c/edit?usp=sharing')]), alt=True, center=True)
write('2025', page('/2025/', 'Women in Agile Tokyo 2025',
                   '2025年2月4日〜5日に大崎ブライトコアホールとオンラインで開催した Women in Agile Tokyo 2025。',
                   'Women in Agile Japan', '2025年2月4日(火)〜5日(水)',
                   [('Venue', '大崎ブライトコアホール + オンライン'), ('Day 1', 'キーノート + 3 トラック'), ('Day 2', 'オープンスペース')],
                   body, 2025))

# ---------- Tokyo 2024 ----------
body = sec('Schedule', 'スケジュール', tl([
    ('9:15', 'Door Open', '受付開始'),
    ('10:00', 'Keynote', '基調講演を行います。'),
    ('11:30', 'Open Spaces + Sessions', 'オープンスペーステクノロジーの説明のあと、トピック提案を行い、オープンスペーステクノロジー形式でセッションを行っていきます(費用が許す範囲でランチを提供します)。並行して、トークセッションも行います。20名程度の会場ですが、オンライン配信を行っていきます。'),
    ('17:30', 'Closing Remarks', 'クロージングを行います。')]))
body += sec('Keynote', '基調講演', speakers([
    dict(img='wia2024-ito.jpg', role='Keynote', name='伊藤 雅充 氏(Masamitsu Ito)',
         org='日本体育大学体育学部教授、博士(学術)、コーチングエクセレンスセンター長',
         title='個が輝く社会に向けて〜スポーツ界での挑戦〜',
         bio=['1971年生まれ、愛媛県出身。2001年3月に東京大学大学院総合文化研究科広域科学専攻生命環境科学系で博士号取得。1998年4月より日本体育大学助手。2002年4月より同大講師、2008年4月より同大准教授。2017年4月より現職。元々はスポーツバイオメカニクスを専門としていたが、かねて関心を持っていたスポーツコーチングに専門を転向。選手本位の「アスリートセンタード・コーチング」を提唱し、これからの時代にあったコーチングの発展・普及、コーチ教育などに取り組んでいる。',
              '国際コーチングエクセレンス評議会コーチング学位基準策定委員、日本体育協会モデル・コア・カリキュラム作成ワーキンググループ委員、日本スポーツ協会公認スポーツ指導者制度検討プロジェクト委員などを歴任。現在は日本パラリンピック委員会強化本部員やスポーツ庁委託事業女性アスリートの育成・支援プロジェクト女性エリートコーチ育成プログラムの運営責任者を務める。']),
]), alt=True)
body += sec('Sponsors and Communities', 'Working Together',
    '        <p class="center">開催趣意書は<a href="https://docs.google.com/presentation/d/1BO8O67FB9CB4P8USBBn_r8qX4L3xGgOGdfmjTAT1MPE/edit?usp=sharing">こちら</a>です。ぜひご支援をご検討くださいませ。</p>\n' + logos([
    ('easg.jpg', 'エンタープライズアジャイル勉強会'),
    ('slalom.png', 'Slalom'), ('productpeople.png', 'ProductPeople'), ('ishiifood.png', '石井食品'),
    ('reiwatravel.png', '株式会社令和トラベル'), ('persol.png', 'パーソルホールディングス'), ('itpreneurs.png', 'ITpreneurs'),
    ('agile-hiyoko.png', 'アジャイルひよこクラブ'), ('scrum-tokyo.png', 'Scrum Tokyo'), ('xpjug.jpg', 'XPJUG 日本XPユーザグループ'),
    ('scrumfest-mikawa.png', 'Scrum Fest Mikawa'), ('agile-japan.png', 'アジャイルジャパン'), ('shinagawa-agile.png', '品川アジャイル'),
    ('isplus.jpg', '株式会社アイズプラス'), ('scrumfest-niigata.png', 'スクラムフェス新潟'), ('devlove.jpg', 'DevLOVE'),
    ('scrumfest-osaka.png', 'Scrum Fest Osaka'), ('community-unicorn.png', '協力コミュニティ'), ('sfs.png', 'SFS'),
    ('scrumfest-okinawa.png', 'Scrum Fest Okinawa'), ('minnano-code.png', 'みんなのコード'), ('innersource-commons.png', 'InnerSource Commons Japan'),
    ('taco.jpg', 'Tokyo Agile Community'), ('smn.png', 'Scrum Masters Night'), ('devopsdays-tokyo.png', 'DevOpsDays Tokyo'),
    ('jasst-tohoku.png', 'JaSST Tohoku')]) +
    f'\n        <p class="note center">前日 2月5日には同会場で <a href="{ALS}eaf-2024/">Enterprise Agile Forum 2024</a> が開催されました。</p>')
body += sec('Links', '関連リンク', links([
    ('ConfEngine', 'https://confengine.com/conferences/women-in-agile-tokyo'),
    ('開催趣意書', 'https://docs.google.com/presentation/d/1BO8O67FB9CB4P8USBBn_r8qX4L3xGgOGdfmjTAT1MPE/edit?usp=sharing')]), alt=True, center=True)
write('2024', page('/2024/', 'Women in Agile Tokyo 2024',
                   '2024年2月6日に大崎ブライトコアホールで開催した Women in Agile Tokyo 2024。',
                   'Women in Agile Japan', '2024年2月6日(火)',
                   [('Venue', '大崎ブライトコアホール 3F'), ('Format', 'オフライン + オンライン配信')], body, 2024))

print('generated: 2026 / osaka-2025 / 2025 / 2024')
