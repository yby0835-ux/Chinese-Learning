from datetime import date, datetime
from zoneinfo import ZoneInfo
from curriculum import CURRICULUM
from kakao import send_message

START_DATE = date(2026, 5, 23)
DAY_KR = ['월', '화', '수', '목', '금', '토', '일']


def build_message():
    now       = datetime.now(ZoneInfo('Asia/Seoul'))
    today     = now.date()
    day_num   = (today - START_DATE).days % len(CURRICULUM)
    lesson    = CURRICULUM[day_num]
    date_str  = f"{now.month}월 {now.day}일"
    day_str   = DAY_KR[now.weekday()]
    total     = len(CURRICULUM)

    lines = [
        f"🇨🇳  오늘의 중국어",
        f"📅  {date_str} ({day_str})  · Day {day_num + 1} / {total}",
        "",
        f"  주제  📌 {lesson['topic']}",
        "",
        "📝  단어",
        "",
    ]

    for w in lesson['words']:
        lines.append(f"  {w['zh']:<6}  {w['pinyin']}")
        lines.append(f"          {w['kr']}")
        lines.append("")

    zh, py, kr = lesson['example']
    lines += [
        "💬  오늘의 표현",
        f"  {zh}",
        f"  {py}",
        f"  {kr}",
        "",
    ]

    gp, gz, gpy, gkr = lesson['grammar']
    lines += [
        "📖  오늘의 문법",
        f"  {gp}",
        "",
        f"  {gz}",
        f"  {gpy}",
        f"  {gkr}",
    ]

    return "\n".join(lines)


if __name__ == '__main__':
    message = build_message()
    print(message)
    send_message(message)
    print("카카오톡 전송 완료")
