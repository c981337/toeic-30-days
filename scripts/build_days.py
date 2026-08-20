#!/usr/bin/env python3
"""Build data/days.js from _parsed_raw.json with vocab, quizzes, phases, and themes."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "_parsed_raw.json"
OUT = ROOT / "data" / "days.js"

THEMES = {
    1: ("Career Fair", "求職面試"),
    2: ("Office Policy", "辦公室政策"),
    3: ("Administrative Support", "行政支援"),
    4: ("Equipment Responsibility", "設備與責任"),
    5: ("Business Communication", "商務溝通"),
    6: ("Arts Leisure", "藝文休閒"),
    7: ("Market Research", "市場調查"),
    8: ("Advertising", "廣告行銷"),
    9: ("Economic Trends", "經濟趨勢"),
    10: ("Retail Shopping", "零售購物"),
    11: ("Technology Innovation", "科技創新"),
    12: ("Factory Production", "工廠生產"),
    13: ("Customer Service", "顧客服務"),
    14: ("Travel Airline", "旅遊航空"),
    15: ("Contracts Negotiation", "合約談判"),
    16: ("Publishing Supply", "出版供應鏈"),
    17: ("Logistics Shipping", "物流運送"),
    18: ("Dining Catering", "餐飲服務"),
    19: ("Finance Revenue", "財務營收"),
    20: ("Budgeting Controls", "預算控管"),
    21: ("Corporate Mergers", "企業併購"),
    22: ("Meetings Conferences", "會議活動"),
    23: ("Events Recognition", "活動表揚"),
    24: ("Promotion Personnel", "晉升人事"),
    25: ("Transit Commuting", "交通通勤"),
    26: ("Banking Accounts", "銀行帳戶"),
    27: ("Investment Portfolio", "投資組合"),
    28: ("Home Property", "居家房產"),
    29: ("Climate Environment", "氣候環保"),
    30: ("Health Medical", "健康醫療"),
}

HEADER_RE = re.compile(
    r"\n*\s*#\s*TOEIC(?:\s+Reading)?[^\n]*(?:\n(?!\n#\s*TOEIC)[^\n]*)*",
    re.IGNORECASE,
)


def phase_for(day: int) -> int:
    if day <= 8:
        return 1
    if day <= 16:
        return 2
    if day <= 24:
        return 3
    return 4


def clean_chinese(text: str) -> str:
    """Strip leaked markdown headers such as '# TOEIC Reading...' and trailing notes."""
    if not text:
        return text
    # Cut from first leaked TOEIC markdown header onward
    m = re.search(r"\n\s*#\s*TOEIC\b", text, flags=re.IGNORECASE)
    if m:
        text = text[: m.start()]
    # Also strip inline leftover file markers
    text = re.sub(r"\[file:\d+\]", "", text)
    return text.rstrip() + ("\n" if text.strip() else "")


# ---------------------------------------------------------------------------
# Authored vocab (12–15) + questions (5) per day — words drawn from each article
# ---------------------------------------------------------------------------

DAY_CONTENT: dict[int, dict] = {
    1: {
        "vocab": [
            {"word": "plentiful", "meaning": "充足的；大量的", "example": "The fair drew a plentiful number of visitors."},
            {"word": "criteria", "meaning": "標準；評選條件", "example": "The main criteria included experience and education."},
            {"word": "reference", "meaning": "推薦人；推薦信", "example": "Each applicant submitted a resume and one reference."},
            {"word": "proficiency", "meaning": "熟練；精通", "example": "Candidates must show communication proficiency."},
            {"word": "aptitude", "meaning": "天賦；性向", "example": "They need the aptitude to work in a fast-changing environment."},
            {"word": "eligible", "meaning": "有資格的", "example": "Degree holders were more likely to be eligible for an interview."},
            {"word": "diligent", "meaning": "勤勉的", "example": "The company also employs diligent and adaptable workers."},
            {"word": "adaptable", "meaning": "適應力強的", "example": "Adaptable applicants often succeed in team projects."},
            {"word": "prospective", "meaning": "預期的；可能的", "example": "One prospective employee felt nervous before the interview."},
            {"word": "apprehensive", "meaning": "憂慮的；不安的", "example": "She felt slightly apprehensive before meeting the hiring team."},
            {"word": "verbal", "meaning": "口頭的", "example": "Several candidates received a verbal job offer."},
            {"word": "accomplishment", "meaning": "成就；成績", "example": "Explain how your accomplishments support long-term goals."},
            {"word": "managerial", "meaning": "管理的；經理級的", "example": "Openings ranged from part-time work to managerial positions."},
            {"word": "trainee", "meaning": "受訓者；實習生", "example": "The firm planned to hire several engineering trainees."},
        ],
        "questions": [
            {
                "q": "根據文章，求職者在與招募團隊會面之前必須提交哪些文件？",
                "choices": ["僅履歷", "申請書、履歷與一封推薦信", "成績單與護照影本", "僅技術證照"],
                "answer": 1,
                "explain": "文中明確提到需送交 application form、resume 與 one reference。",
            },
            {
                "q": "本文的主要重點最接近下列哪一項？",
                "choices": ["介紹西橋會議中心的建築風格", "說明就業博覽會的招募流程與錄用條件", "比較各大學科系的就業率", "批評公司薪資過低"],
                "answer": 1,
                "explain": "全文圍繞職博會、申請條件、面試與錄用通知展開。",
            },
            {
                "q": "關於公司錄用標準，下列何者可由文中合理推論？",
                "choices": ["只錄用成績頂尖者", "實務經驗與團隊合作能力也會被重視", "沒有學位者完全無法面試", "口頭錄用沒有法律效力所以不被使用"],
                "answer": 1,
                "explain": "招募人員表示除學業表現外，也會考慮勤勉、適應力與團隊專案經驗。",
            },
            {
                "q": "文中 “apprehensive” 在語境中最接近什麼意思？",
                "choices": ["興奮的", "憂慮不安的", "漠不關心的", "憤怒的"],
                "answer": 1,
                "explain": "應徵者在面試前感到 slightly apprehensive，但仍保持希望，表示緊張不安。",
            },
            {
                "q": "人資經理特別欣賞哪一類應徵者？",
                "choices": ["只談未來夢想的人", "能清楚說明過去成就並連結公司長期目標的人", "拒絕接受訓練的人", "只申請兼職的人"],
                "answer": 1,
                "explain": "文末指出公司對能辨識過去成就並說明如何支持長期目標的申請者印象深刻。",
            },
        ],
    },
    2: {
        "vocab": [
            {"word": "revised", "meaning": "修訂的；更新的", "example": "The legal department issued a revised office policy."},
            {"word": "comply", "meaning": "遵守", "example": "Several employees failed to comply with the dress code."},
            {"word": "attire", "meaning": "服裝；裝束", "example": "Staff must wear proper business attire on duty."},
            {"word": "inspection", "meaning": "檢查；視察", "example": "A recent inspection found supplies left in open areas."},
            {"word": "procedure", "meaning": "程序；步驟", "example": "The company introduced a standard procedure for document control."},
            {"word": "enforce", "meaning": "執行；強制實施", "example": "Team leaders were told to enforce the rule consistently."},
            {"word": "confidential", "meaning": "機密的", "example": "The system is intended to protect confidential information."},
            {"word": "adhere", "meaning": "遵守；堅持", "example": "Staff members must adhere to the arrangement."},
            {"word": "refrain", "meaning": "克制；避免", "example": "Employees must refrain from entering restricted areas."},
            {"word": "obligation", "meaning": "義務；責任", "example": "The company has a legal obligation to maintain security."},
            {"word": "prohibited", "meaning": "被禁止的", "example": "Damaging acts may be limited or prohibited."},
            {"word": "compliance", "meaning": "合規；遵循", "example": "A law firm reviews corporate compliance matters."},
            {"word": "restricted", "meaning": "受限制的", "example": "Do not enter restricted areas without permission."},
        ],
        "questions": [
            {
                "q": "公司為何發布修訂後的辦公室政策？",
                "choices": ["為了增加休假天數", "因為有員工未遵守服裝與訪客進出規定", "因為要擴大辦公空間", "因為法務部即將裁員"],
                "answer": 1,
                "explain": "開頭說明員工未能遵守 dress code 與 visitor access rules。",
            },
            {
                "q": "本文主要在說明什麼？",
                "choices": ["如何設計新制服", "新辦公室安全與合規規定及其目的", "如何申請訪客證的細節表格", "法律事務所的收費標準"],
                "answer": 1,
                "explain": "文章聚焦新規定、標準流程與保護機密資訊的目的。",
            },
            {
                "q": "若發生緊急情況或疑似竊盜，員工應怎麼做？",
                "choices": ["自行處理後再回報", "立即通報", "先離開辦公室再說", "等到下班再寫報告"],
                "answer": 1,
                "explain": "通知要求立即報告，而不是獨自解決。",
            },
            {
                "q": "文中 “adhere to” 最接近下列哪一意思？",
                "choices": ["忽略", "遵守", "批評", "延後"],
                "answer": 1,
                "explain": "Staff must adhere to the arrangement 表示必須遵守該安排。",
            },
            {
                "q": "管理層對新規定的態度最接近？",
                "choices": ["認為短期嚴格但長期有正面效果", "打算立即取消", "完全不在意員工意見", "只為了應付外部稽核一次"],
                "answer": 0,
                "explain": "雖然有人覺得嚴格，但管理層強調長期會有正面效果。",
            },
        ],
    },
    3: {
        "vocab": [
            {"word": "administrative", "meaning": "行政的", "example": "The administrative division begins work before rush hour."},
            {"word": "pending", "meaning": "待處理的", "example": "She organizes pending paperwork in the correct section."},
            {"word": "deadline", "meaning": "截止日期", "example": "Mina prepared to send the file before the noon deadline."},
            {"word": "acquaint", "meaning": "使熟悉", "example": "The workshop helped acquaint staff with filing methods."},
            {"word": "demanding", "meaning": "要求高的；吃力的", "example": "The training was demanding but useful."},
            {"word": "accustomed", "meaning": "習慣於", "example": "Staff became more accustomed to company expectations."},
            {"word": "efficiently", "meaning": "有效率地", "example": "Workers should perform assignments efficiently."},
            {"word": "attentively", "meaning": "專心地；仔細地", "example": "Monitor details attentively under pressure."},
            {"word": "extension", "meaning": "延期；延長", "example": "Notify the team if an extension is needed."},
            {"word": "reluctant", "meaning": "不情願的", "example": "Mina was a little reluctant at first."},
            {"word": "workshop", "meaning": "研討會；工作坊", "example": "The supervisor held a short workshop for new staff."},
            {"word": "electronically", "meaning": "以電子方式", "example": "She sent the file electronically to the manager."},
            {"word": "concentrate", "meaning": "專注", "example": "Those who can concentrate under pressure may be promoted."},
        ],
        "questions": [
            {
                "q": "Mina 今天早上被要求完成什麼任務？",
                "choices": ["安排員工旅遊", "編輯產品資訊並提交給行銷經理", "面試新進員工", "維修所有印表機"],
                "answer": 1,
                "explain": "她被要求 edit product information 並直接交給 marketing manager。",
            },
            {
                "q": "主管舉辦研討會的主要目的是？",
                "choices": ["慶祝業績", "讓大家熟悉內部歸檔方法", "宣布裁員", "更換辦公家具"],
                "answer": 1,
                "explain": "研討會是為了 acquaint everyone with internal filing methods。",
            },
            {
                "q": "關於 Mina，下列何者正確？",
                "choices": ["她一直很樂意接任務", "她起初有些不情願，但後來獨自完成並看見其價值", "她錯過了中午截止時間", "她拒絕參加訓練"],
                "answer": 1,
                "explain": "文中說她 initially reluctant，但下午已獨立完成任務。",
            },
            {
                "q": "“accustomed to” 在文中意思最接近？",
                "choices": ["害怕", "習慣於", "反對", "忘記"],
                "answer": 1,
                "explain": "become more accustomed to expectations 表示更習慣公司期待。",
            },
            {
                "q": "經理認為什麼樣的員工較可能升遷？",
                "choices": ["常請假的人", "能在壓力下專心工作的人", "只做簡單工作的人", "不回覆電話的人"],
                "answer": 1,
                "explain": "文中指出能 concentrate under pressure 者可能進入更高職位。",
            },
        ],
    },
    4: {
        "vocab": [
            {"word": "directory", "meaning": "通訊錄；目錄", "example": "He was asked to update the directory."},
            {"word": "uploaded", "meaning": "已上傳的", "example": "He checked whether the latest files had been uploaded."},
            {"word": "duplicate", "meaning": "副本；複製本", "example": "He made a duplicate of the missing page."},
            {"word": "lax", "meaning": "鬆懈的", "example": "Employees should never become lax with confidential files."},
            {"word": "procrastinate", "meaning": "拖延", "example": "Do not procrastinate when handling confidential information."},
            {"word": "accountable", "meaning": "應負責的", "example": "Each person is accountable for work quality."},
            {"word": "coordinate", "meaning": "協調", "example": "He helped coordinate the schedule for the meeting."},
            {"word": "skillfully", "meaning": "熟練地", "example": "He handled the client visit skillfully."},
            {"word": "foster", "meaning": "培養；促進", "example": "Careful work can foster trust in the office."},
            {"word": "confidential", "meaning": "機密的", "example": "Never be lax when handling confidential information."},
            {"word": "reception", "meaning": "接待處", "example": "Materials were arranged next to the reception desk."},
            {"word": "keypad", "meaning": "數字鍵盤", "example": "He checked her visitor code on the keypad."},
            {"word": "consistently", "meaning": "一致地；持續地", "example": "Tasks done carefully and consistently build trust."},
        ],
        "questions": [
            {
                "q": "新員工開始任務前必須先做什麼？",
                "choices": ["打掃停車場", "登入伺服器並檢查最新檔案是否已上傳", "召開全公司會議", "更換所有書櫃"],
                "answer": 1,
                "explain": "他必須 log on to the company server 並確認 files uploaded。",
            },
            {
                "q": "組長特別提醒員工不要有什麼行為？",
                "choices": ["準時上班", "鬆懈或拖延，尤其在處理機密資訊時", "協助客戶", "更新通訊錄"],
                "answer": 1,
                "explain": "文中說 never become lax or procrastinate，尤其處理機密時。",
            },
            {
                "q": "客戶到訪時，這名員工做了哪些事？",
                "choices": ["只請客戶自行等待", "打招呼、核對訪客代碼並協助協調行程", "拒絕接待", "立刻結束會議"],
                "answer": 1,
                "explain": "他 greet、check visitor code，並協助收集文件與協調時程。",
            },
            {
                "q": "文中 “accountable” 最接近？",
                "choices": ["可選的", "應負責的", "暫時的", "秘密的"],
                "answer": 1,
                "explain": "Each person is accountable for quality 表示對品質負責。",
            },
            {
                "q": "辦公室主任最後想傳達的訊息是？",
                "choices": ["小任務無關緊要", "仔細一致地完成小任務也能促進信任", "只需追求速度", "機密文件可以隨意放置"],
                "answer": 1,
                "explain": "即使簡單動作，仔細一致執行也能 foster trust。",
            },
        ],
    },
    5: {
        "vocab": [
            {"word": "briefcase", "meaning": "公事包", "example": "The traveler arrived with a briefcase and folders."},
            {"word": "timetable", "meaning": "時間表", "example": "He brought a timetable for the urgent mission."},
            {"word": "compile", "meaning": "彙整；編纂", "example": "The staff decided to compile the data promptly."},
            {"word": "timely", "meaning": "及時的", "example": "They needed to provide timely feedback."},
            {"word": "accessible", "meaning": "易取得的；易懂的", "example": "The final outline should be clear and accessible."},
            {"word": "expertise", "meaning": "專業知識", "example": "Everyone was asked to work with expertise."},
            {"word": "implement", "meaning": "實施；執行", "example": "The company planned to implement a new system permanently."},
            {"word": "revise", "meaning": "修訂", "example": "The material must be revised before the next forum."},
            {"word": "compliance", "meaning": "遵循；合規", "example": "Good office work depends on careful compliance."},
            {"word": "clarify", "meaning": "澄清；說明清楚", "example": "They must clarify each aspect of the project."},
            {"word": "coordination", "meaning": "協調", "example": "Strong coordination helps complete complex work."},
            {"word": "concealed", "meaning": "被隱藏的", "example": "They prepared replacements in case files were concealed."},
            {"word": "forum", "meaning": "論壇；研討會", "example": "Materials must be ready before the next forum."},
        ],
        "questions": [
            {
                "q": "商務旅客抵達辦公室後首先做了什麼？",
                "choices": ["立刻召開董事會", "查看信箱、閱讀公告並準備向團隊說明任務", "取消所有報告", "更換檔案櫃"],
                "answer": 1,
                "explain": "他 checked email、reviewed announcement，並準備 explain remaining tasks。",
            },
            {
                "q": "部門對最終大綱的要求是？",
                "choices": ["越長越好", "清楚、可存取且切合現實", "只給主管看", "完全不需修訂"],
                "answer": 1,
                "explain": "希望 outline clear, accessible, and realistic。",
            },
            {
                "q": "為何報告資料必須在下次論壇前修訂？",
                "choices": ["因為公司要永久實施新系統", "因為要關閉部門", "因為沒有助理", "因為客戶取消合約"],
                "answer": 0,
                "explain": "經理指出公司計畫 permanently implement a new system。",
            },
            {
                "q": "“compile” 在文中意思最接近？",
                "choices": ["刪除", "彙整", "隱藏", "延後"],
                "answer": 1,
                "explain": "compile the data promptly 指迅速彙整資料。",
            },
            {
                "q": "講者在會議中強調什麼態度？",
                "choices": ["逃避改變", "直接面對改變並自信說明計畫", "完全依賴外部顧問", "停止所有協調"],
                "answer": 1,
                "explain": "公司必須 face changes directly 並 speak with confidence。",
            },
        ],
    },
    6: {
        "vocab": [
            {"word": "exhibition", "meaning": "展覽", "example": "The gallery announced a weekend exhibition."},
            {"word": "alumni", "meaning": "校友", "example": "Many alumni from the art museum planned to attend."},
            {"word": "manuscript", "meaning": "手稿", "example": "A new edition of her manuscript will appear next month."},
            {"word": "proceeds", "meaning": "收益；所得", "example": "Proceeds from the sale support a library donation program."},
            {"word": "admission", "meaning": "入場許可；入場費", "example": "Admission was required for the banquet."},
            {"word": "antique", "meaning": "古董的；古董", "example": "Tickets included antique items on display."},
            {"word": "anonymous", "meaning": "匿名的", "example": "The show was not anonymous publicity."},
            {"word": "fascinating", "meaning": "引人入勝的", "example": "The event was designed to be informative and fascinating."},
            {"word": "subscription", "meaning": "訂閱", "example": "The next subscription would begin soon."},
            {"word": "leisure", "meaning": "休閒", "example": "The event combined sightseeing and outdoor leisure."},
            {"word": "banquet", "meaning": "宴會", "example": "Admission was required for the banquet."},
            {"word": "contribution", "meaning": "貢獻", "example": "Many saw the event as a meaningful cultural contribution."},
            {"word": "journal", "meaning": "期刊；雜誌", "example": "The current issue of the journal was available."},
        ],
        "questions": [
            {
                "q": "週末展覽結合了哪些活動？",
                "choices": ["僅靜態畫展", "觀光、現場音樂與戶外休閒", "只有企業面試", "只有拍賣會"],
                "answer": 1,
                "explain": "活動結合 sightseeing, live music, and outdoor leisure。",
            },
            {
                "q": "知名作家演講提到書款用途是？",
                "choices": ["翻修戲院", "支持公共圖書館捐贈計畫", "購買腳踏車", "支付匿名廣告"],
                "answer": 1,
                "explain": "proceeds 將支持 donation program for the public library。",
            },
            {
                "q": "關於這場活動的性質，主辦者怎麼說？",
                "choices": ["只是匿名宣傳", "經精心規劃，具資訊性與地方公益價值", "臨時決定的野餐", "僅限校友參加"],
                "answer": 1,
                "explain": "他說不是 anonymous publicity，而是 carefully planned 且 beneficial。",
            },
            {
                "q": "“proceeds” 在文中指的是？",
                "choices": ["手續", "銷售所得", "入場券", "手稿草稿"],
                "answer": 1,
                "explain": "proceeds from the sale 指銷售收益。",
            },
            {
                "q": "到了傍晚，參與者對活動的評價偏向？",
                "choices": ["只覺得吵雜", "認為既娛樂又對文化生活有意義", "要求退票", "覺得與藝文無關"],
                "answer": 1,
                "explain": "許多人說不僅 entertaining，也是 meaningful cultural contribution。",
            },
        ],
    },
    7: {
        "vocab": [
            {"word": "survey", "meaning": "調查", "example": "The PR department conducted a survey on seasonal campaigns."},
            {"word": "respondent", "meaning": "受訪者", "example": "Respondent data showed intense competition."},
            {"word": "demonstration", "meaning": "示範；展示", "example": "Buyers preferred clear demonstrations over informal ads."},
            {"word": "aggressively", "meaning": "積極地；侵略性地", "example": "The firm raised its target more aggressively."},
            {"word": "utmost", "meaning": "最大努力", "example": "The team should do its utmost to produce a presentation."},
            {"word": "publicize", "meaning": "宣傳", "example": "The brand would publicize a new promotion."},
            {"word": "postponed", "meaning": "被延後的", "example": "The plan was not postponed by management."},
            {"word": "rival", "meaning": "競爭對手", "example": "The effort would create an advantage over rivals."},
            {"word": "ambitious", "meaning": "有野心的；野心勃勃的", "example": "Although the campaign was ambitious, results were promising."},
            {"word": "promising", "meaning": "有前景的", "example": "The results of the campaign were promising."},
            {"word": "examine", "meaning": "檢視；審查", "example": "Closely examine consumer behavior across departments."},
            {"word": "consistently", "meaning": "持續一致地", "example": "Growth would be steady if the team followed the plan consistently."},
            {"word": "marketplace", "meaning": "市場", "example": "The company expanded its marketplace strategy."},
        ],
        "questions": [
            {
                "q": "調查顯示買家較偏好什麼？",
                "choices": ["非正式廣告", "清楚的示範說明", "完全不看宣傳", "只看價格標籤"],
                "answer": 1,
                "explain": "受訪者資料顯示偏好 clear demonstrations rather than informal advertising。",
            },
            {
                "q": "根據分析，公司決定採取什麼策略？",
                "choices": ["縮減市場", "擴大市場策略並更積極提高目標", "停止所有促銷", "延後所有簡報"],
                "answer": 1,
                "explain": "公司 expand marketplace strategy 並 raise target aggressively。",
            },
            {
                "q": "為何計畫沒有延後？",
                "choices": ["因為資源不足", "管理層相信努力會正面影響銷售並勝過對手", "因為法律禁止延後", "因為 CEO 出差"],
                "answer": 1,
                "explain": "management believed the effort would affect sales positively。",
            },
            {
                "q": "“utmost” 在 do its utmost 中意思是？",
                "choices": ["最小", "最大努力", "普通", "隨意"],
                "answer": 1,
                "explain": "do its utmost 表示竭盡所能。",
            },
            {
                "q": "CEO 總結時強調什麼？",
                "choices": ["忽略消費者行為", "聚焦實際改變並跨部門合作", "只靠線上比較圖表", "停止檢視績效差距"],
                "answer": 1,
                "explain": "他要求 focus on practical changes、examine behavior 並 cooperate。",
            },
        ],
    },
    8: {
        "vocab": [
            {"word": "campaign", "meaning": "行銷活動；宣傳活動", "example": "The bookstore launched a celebration campaign."},
            {"word": "experiment", "meaning": "實驗", "example": "Staff observed customers in a small experiment."},
            {"word": "advertisement", "meaning": "廣告", "example": "The advertisement should attract attention instantly."},
            {"word": "strategy", "meaning": "策略", "example": "Introduce the product with a simple strategy."},
            {"word": "disregard", "meaning": "忽視；不理會", "example": "Do not disregard the importance of brand image."},
            {"word": "initial", "meaning": "最初的", "example": "The initial message should cover customer needs."},
            {"word": "detect", "meaning": "偵測；察覺", "example": "Detect consumer preferences accurately."},
            {"word": "appealing", "meaning": "吸引人的", "example": "Visitors believed the display was obviously appealing."},
            {"word": "incentive", "meaning": "誘因；激勵", "example": "A strong incentive helps the team master the market."},
            {"word": "subscribe", "meaning": "訂閱", "example": "Explain the advantage of subscribing early."},
            {"word": "majority", "meaning": "大多數", "example": "The majority of shoppers prefer creative promotions."},
            {"word": "resolve", "meaning": "解決", "example": "Every effort should be made to resolve doubts favorably."},
            {"word": "impact", "meaning": "影響；衝擊", "example": "Accurate preference detection strengthens campaign impact."},
        ],
        "questions": [
            {
                "q": "書店慶祝活動一開始做了什麼實驗？",
                "choices": ["測試收銀系統速度", "觀察顧客對陳列、樣品與銷售目標的反應", "統計員工出勤", "關閉店面整修"],
                "answer": 1,
                "explain": "員工觀察顧客對 displays、samples 與 sales target 的反應。",
            },
            {
                "q": "行銷團隊認為廣告最重要的是？",
                "choices": ["越長越好", "立即吸引注意力", "完全不提訂閱", "只放文字不含圖像"],
                "answer": 1,
                "explain": "廣告應 attract attention instantly。",
            },
            {
                "q": "分析師特別提醒不要忽視什麼？",
                "choices": ["店面租金", "品牌形象的重要性", "攝影師請假", "作者簽名數量"],
                "answer": 1,
                "explain": "must not disregard the importance of brand image。",
            },
            {
                "q": "文中 “disregard” 意思最接近？",
                "choices": ["強調", "忽視", "測量", "慶祝"],
                "answer": 1,
                "explain": "disregard 表示忽視、不理會。",
            },
            {
                "q": "團隊最後認為最佳成果來自什麼？",
                "choices": ["偶然運氣", "穩定努力、清楚目標與強而有力的誘因", "只靠彩色陳列", "縮短營業時間"],
                "answer": 1,
                "explain": "best results come from steady effort, clear goals, and strong incentive。",
            },
        ],
    },
    9: {
        "vocab": [
            {"word": "enterprise", "meaning": "企業", "example": "The enterprise had experienced a rise and fall in demand."},
            {"word": "optimistic", "meaning": "樂觀的", "example": "The director said the situation remained optimistic."},
            {"word": "unstable", "meaning": "不穩定的", "example": "The industry was healthy despite unstable months."},
            {"word": "boom", "meaning": "繁榮；景氣高漲", "example": "The report showed evidence of a possible boom."},
            {"word": "merge", "meaning": "合併", "example": "The company decided to merge with a private partner."},
            {"word": "substantial", "meaning": "可觀的；重大的", "example": "The contribution to future growth would be substantial."},
            {"word": "prosperity", "meaning": "繁榮", "example": "Prosperity could wane if long-term consequences are ignored."},
            {"word": "wane", "meaning": "衰退；減弱", "example": "Prosperity could wane without careful planning."},
            {"word": "depression", "meaning": "蕭條；不景氣", "example": "A stagnant market may cause an unexpected depression."},
            {"word": "stagnant", "meaning": "停滯的", "example": "Economic conditions can change if the market becomes stagnant."},
            {"word": "productivity", "meaning": "生產力", "example": "The firm promised to boost productivity."},
            {"word": "efficient", "meaning": "有效率的", "example": "Remain economically efficient in the coming period."},
            {"word": "prospect", "meaning": "前景", "example": "Keep a close eye on the prospect for the coming period."},
            {"word": "indicator", "meaning": "指標", "example": "Every indicator must be reviewed carefully."},
        ],
        "questions": [
            {
                "q": "執行長宣布調整營業時間的目的是？",
                "choices": ["減少員工", "加快交易並提升整體服務", "關閉分支機構", "停止生產"],
                "answer": 1,
                "explain": "調整是為了 speed up trading and improve overall service。",
            },
            {
                "q": "公司決定採取哪種成長策略？",
                "choices": ["繼續單打獨鬥", "與私人合作夥伴合併", "全面外包", "停止投資"],
                "answer": 1,
                "explain": "decided to merge with a private partner rather than continue alone。",
            },
            {
                "q": "主管對繁榮提出什麼警告？",
                "choices": ["繁榮永遠不會改變", "若忽略長期後果，繁榮可能衰退", "指標不必檢視", "市場停滯沒有影響"],
                "answer": 1,
                "explain": "prosperity could wane if long-term consequences are ignored。",
            },
            {
                "q": "“wane” 在文中意思最接近？",
                "choices": ["增加", "減弱／衰退", "保持不變", "突然開始"],
                "answer": 1,
                "explain": "wane 表示逐漸減弱或衰退。",
            },
            {
                "q": "會議結束時公司承諾什麼？",
                "choices": ["忽視前景", "提升生產力、維持效率並關注前景", "停止合併談判", "提高所有營運成本"],
                "answer": 1,
                "explain": "承諾 boost productivity、remain efficient 並關注 prospect。",
            },
        ],
    },
    10: {
        "vocab": [
            {"word": "cashier", "meaning": "收銀員", "example": "The cashier reminded customers about the tax-free promotion."},
            {"word": "promotion", "meaning": "促銷", "example": "The store was offering a tax-free promotion for a limited time."},
            {"word": "affordable", "meaning": "負擔得起的", "example": "She compared a brand with a more affordable alternative."},
            {"word": "warranty", "meaning": "保固", "example": "The assistant explained the price, warranty, and receipt process."},
            {"word": "authentic", "meaning": "真正的；正品的", "example": "The vendor could provide an authentic product."},
            {"word": "installment", "meaning": "分期付款", "example": "She decided to purchase the item in installments."},
            {"word": "clearance", "meaning": "清倉", "example": "The store offered clearance discounts."},
            {"word": "redeemable", "meaning": "可兌換的", "example": "Regular subscribers received redeemable benefits."},
            {"word": "subscriber", "meaning": "訂戶；會員", "example": "Benefits were available for regular subscribers."},
            {"word": "receipt", "meaning": "收據", "example": "Ask about the warranty and receipt process carefully."},
            {"word": "vendor", "meaning": "供應商；販售者", "example": "The vendor could provide a similar model if preferred."},
            {"word": "alternative", "meaning": "替代方案", "example": "She compared the brand with an affordable alternative."},
            {"word": "convenient", "meaning": "便利的", "example": "The shopping experience remained convenient for visitors."},
        ],
        "questions": [
            {
                "q": "收銀員提醒顧客商店正在提供什麼限時優惠？",
                "choices": ["免費送貨永久有效", "免稅促銷", "買一送一全部商品", "會員終身免年費"],
                "answer": 1,
                "explain": "商店 offering a tax-free promotion for a limited time。",
            },
            {
                "q": "顧客為何選擇分期購買？",
                "choices": ["因為商品缺貨", "因為分期收費方式較容易接受", "因為店員拒絕一次付清", "因為沒有保固"],
                "answer": 1,
                "explain": "she purchased in installments because the charge was more acceptable。",
            },
            {
                "q": "關於另一位在超市的顧客，文中提到什麼？",
                "choices": ["完全不看標籤", "檢查標籤並閱讀產品說明後再決定", "只買最貴商品", "拒絕任何折扣"],
                "answer": 1,
                "explain": "另一位顧客 checking labels and reading descriptions before choosing。",
            },
            {
                "q": "“authentic” 在文中最接近？",
                "choices": ["仿冒的", "正品／真正的", "過期的", "免費的"],
                "answer": 1,
                "explain": "authentic product 指真正的正品。",
            },
            {
                "q": "打烊時商店成功維持了什麼？",
                "choices": ["混亂的貨架", "整齊貨架、吸引人的陳列與便利購物體驗", "停止所有促銷", "關閉雜貨區"],
                "answer": 1,
                "explain": "kept shelves tidy、displays attractive，且體驗 convenient。",
            },
        ],
    },
    11: {
        "vocab": [
            {"word": "domestic", "meaning": "國內的", "example": "A domestic technology firm presented a new device."},
            {"word": "invention", "meaning": "發明", "example": "The invention was handmade in the laboratory."},
            {"word": "breakdown", "meaning": "故障；損壞", "example": "It was tested repeatedly to avoid any breakdown."},
            {"word": "revolutionary", "meaning": "革命性的", "example": "The product featured a revolutionary sensor."},
            {"word": "innovative", "meaning": "創新的", "example": "It included an innovative control system."},
            {"word": "durable", "meaning": "耐用的", "example": "The device was made of durable materials."},
            {"word": "patent", "meaning": "專利", "example": "The team intended to extend the patent."},
            {"word": "upgrade", "meaning": "升級", "example": "They would upgrade the appearance after feedback."},
            {"word": "corrosion", "meaning": "腐蝕", "example": "The concept was improved to reduce corrosion."},
            {"word": "compatible", "meaning": "相容的", "example": "The technology was compatible with existing systems."},
            {"word": "distribution", "meaning": "通路；配銷", "example": "The product would be available for international distribution."},
            {"word": "reliable", "meaning": "可靠的", "example": "The team believed the device was accurate and reliable."},
            {"word": "availability", "meaning": "可用性；供貨情況", "example": "They discussed the availability of updated versions."},
        ],
        "questions": [
            {
                "q": "新裝置的設計目的是？",
                "choices": ["取代所有交通工具", "提升家用電器品質", "只做實驗室展示", "降低專利費用"],
                "answer": 1,
                "explain": "designed to improve the quality of home appliances。",
            },
            {
                "q": "說明書指出該裝置有什麼特點？",
                "choices": ["只能在簡單環境使用", "由耐用材料製成，複雜環境也能安全使用", "無法升級外觀", "與現有系統不相容"],
                "answer": 1,
                "explain": "made of durable materials and safe even in complicated environments。",
            },
            {
                "q": "工程師提到設計靈感與改良重點為何？",
                "choices": ["靈感來自歷史發現，並改良以減少腐蝕", "完全抄襲競爭對手", "取消感測器", "停止投資開發"],
                "answer": 0,
                "explain": "inspired by a historic discovery，並 improved to reduce corrosion。",
            },
            {
                "q": "“compatible” 意思最接近？",
                "choices": ["互相排斥", "相容可用", "過時", "昂貴"],
                "answer": 1,
                "explain": "compatible with existing systems 表示與現有系統相容。",
            },
            {
                "q": "會議結束時投資人與公司下一步計畫為何？",
                "choices": ["立即結束專案", "多位投資人表示興趣，並計畫後續會議討論下一階段", "拒絕國內銷售", "銷毀原型"],
                "answer": 1,
                "explain": "investors expressed interest；公司計畫 follow-up meeting。",
            },
        ],
    },
    12: {
        "vocab": [
            {"word": "renovate", "meaning": "翻修", "example": "The manufacturer plans to renovate its underground facility."},
            {"word": "automate", "meaning": "使自動化", "example": "They will automate several production lines."},
            {"word": "attributed", "meaning": "歸因於", "example": "The decision was attributed to a shortage of materials."},
            {"word": "shortage", "meaning": "短缺", "example": "A shortage of raw materials drove the renovation."},
            {"word": "flexible", "meaning": "有彈性的", "example": "Equipment was composed of flexible components."},
            {"word": "specification", "meaning": "規格", "example": "Every process must follow strict specifications."},
            {"word": "precaution", "meaning": "預防措施", "example": "Safety precautions were essential in the plant."},
            {"word": "economize", "meaning": "節省", "example": "The company aimed to economize on power."},
            {"word": "modification", "meaning": "修改；改良", "example": "The modification would increase productivity."},
            {"word": "expiration", "meaning": "到期；效期", "example": "The expiration date for components would be monitored."},
            {"word": "comparable", "meaning": "可比較的；相當的", "example": "Manufacturing capacity was comparable to other factories."},
            {"word": "assemble", "meaning": "組裝", "example": "Workers were trained to assemble parts separately."},
            {"word": "productivity", "meaning": "生產力", "example": "The modification would increase productivity."},
        ],
        "questions": [
            {
                "q": "製造商翻修並自動化生產線的原因是？",
                "choices": ["員工過多", "原物料短缺與提升效率需求", "客戶要求關閉工廠", "土地租約到期"],
                "answer": 1,
                "explain": "attributed to shortage of raw materials and need to improve efficiency。",
            },
            {
                "q": "檢查期間主管發現什麼問題？",
                "choices": ["工廠因化學品洩漏受損，部分工具有刮痕", "完全沒有安全問題", "訂單已全部取消", "機器過多無法放置"],
                "answer": 0,
                "explain": "plant damaged by chemical leak；tools had scratches。",
            },
            {
                "q": "工程師提到公司在節能方面的目標是？",
                "choices": ["增加用電", "節約電力並減少浪費", "忽略零件效期", "降低生產力"],
                "answer": 1,
                "explain": "aimed to economize on power and reduce waste。",
            },
            {
                "q": "“attributed to” 意思最接近？",
                "choices": ["無關", "歸因於", "反對", "隱藏"],
                "answer": 1,
                "explain": "decision was attributed to... 表示歸因於……。",
            },
            {
                "q": "主管認為專案成功取決於什麼？",
                "choices": ["運氣", "仔細規劃與跨部門緊密合作", "取消訓練", "停止監控效期"],
                "answer": 1,
                "explain": "success depended on careful planning and strong cooperation。",
            },
        ],
    },
    13: {
        "vocab": [
            {"word": "representative", "meaning": "代表；客服專員", "example": "A customer service representative received complaints."},
            {"word": "defective", "meaning": "有瑕疵的", "example": "Customers complained about a defective product."},
            {"word": "courteously", "meaning": "有禮貌地", "example": "The agent responded courteously to the caller."},
            {"word": "appropriately", "meaning": "適當地", "example": "She promised to handle the deal appropriately."},
            {"word": "inconvenience", "meaning": "不便", "example": "She apologized for the inconvenience."},
            {"word": "assured", "meaning": "向……保證", "example": "She assured the client the issue would be resolved."},
            {"word": "evaluation", "meaning": "評估", "example": "Evaluation of the complaint would be completed promptly."},
            {"word": "promptly", "meaning": "迅速地", "example": "A notification would be sent as soon as possible."},
            {"word": "disclose", "meaning": "揭露；公開", "example": "Disclose all relevant information politely."},
            {"word": "guarantee", "meaning": "保證", "example": "The company must guarantee a positive experience."},
            {"word": "commitment", "meaning": "承諾；投入", "example": "Their commitment to quality service made a difference."},
            {"word": "satisfaction", "meaning": "滿意度", "example": "Satisfaction depended on clear communication."},
            {"word": "replace", "meaning": "更換", "example": "The company would replace the product if necessary."},
        ],
        "questions": [
            {
                "q": "顧客投訴的內容是什麼？",
                "choices": ["價格太高", "商品不完整且包裝商標略有損壞", "外送太慢", "客服沒有接電話"],
                "answer": 1,
                "explain": "item not complete；logo on packaging slightly damaged。",
            },
            {
                "q": "客服承諾如何處理？",
                "choices": ["拒絕退換", "更換商品，必要時退款", "要求顧客自行維修", "轉售瑕疵品"],
                "answer": 1,
                "explain": "company would replace the product and return payment if necessary。",
            },
            {
                "q": "主管提醒團隊互動時應注意什麼？",
                "choices": ["對來電者不耐煩", "自信互動並有禮貌地公開相關資訊", "隱瞞所有資訊", "只寄簡訊不通話"],
                "answer": 1,
                "explain": "interact confidently 並 disclose information politely。",
            },
            {
                "q": "“courteously” 意思最接近？",
                "choices": ["粗魯地", "有禮貌地", "匆忙地", "冷淡地"],
                "answer": 1,
                "explain": "responded courteously 表示有禮貌地回應。",
            },
            {
                "q": "輪班結束時的結果顯示什麼？",
                "choices": ["沒有案件解決", "數起案件成功解決，服務承諾發揮作用", "全體客服離職", "公司停止保證服務"],
                "answer": 1,
                "explain": "several cases solved successfully；commitment made a difference。",
            },
        ],
    },
    14: {
        "vocab": [
            {"word": "itinerary", "meaning": "行程表", "example": "He arrived with a detailed itinerary."},
            {"word": "customs", "meaning": "海關", "example": "Fill out the customs form before entry."},
            {"word": "declare", "meaning": "申報", "example": "Declare any items that might be subject to duty."},
            {"word": "duty", "meaning": "關稅", "example": "Some items may be subject to duty."},
            {"word": "boarded", "meaning": "登機；上船", "example": "The passenger boarded the flight in business class."},
            {"word": "carrier", "meaning": "承運業者；航空公司", "example": "He contacted the carrier about missing baggage."},
            {"word": "locate", "meaning": "找到；定位", "example": "He asked them to locate the suitcase promptly."},
            {"word": "hospitality", "meaning": "款待；好客", "example": "He decided to indulge in the local hospitality."},
            {"word": "proximity", "meaning": "接近；鄰近", "example": "Proximity to attractions made the trip enjoyable."},
            {"word": "exotic", "meaning": "異國風情的", "example": "He visited several exotic locations."},
            {"word": "superb", "meaning": "極好的", "example": "He said the experience was superb."},
            {"word": "baggage", "meaning": "行李", "example": "Upon arrival, his baggage was missing."},
            {"word": "destination", "meaning": "目的地", "example": "He enjoyed a comfortable journey to his destination."},
        ],
        "questions": [
            {
                "q": "代理人員提醒旅客必須做什麼？",
                "choices": ["放棄護照", "填寫海關表格並申報可能課稅物品", "改搭經濟艙", "取消行程"],
                "answer": 1,
                "explain": "fill out customs form and declare items subject to duty。",
            },
            {
                "q": "抵達後旅客遇到什麼問題？",
                "choices": ["護照遺失", "行李遺失", "班機取消", "飯店超訂"],
                "answer": 1,
                "explain": "noticed that his baggage was missing。",
            },
            {
                "q": "航空公司人員如何回應行李問題？",
                "choices": ["拒絕協助", "致歉並承諾盡快將行李送到飯店", "要求旅客自行尋找", "只退部分票價"],
                "answer": 1,
                "explain": "apologized and promised to ship luggage to his hotel。",
            },
            {
                "q": "“proximity” 在文中意思最接近？",
                "choices": ["距離遙遠", "鄰近／接近", "昂貴", "危險"],
                "answer": 1,
                "explain": "proximity to attractions 指靠近景點。",
            },
            {
                "q": "旅客對整體旅程的評價是？",
                "choices": ["覺得不值得長途飛行", "認為壯麗景色與多元文化值得這趟飛行", "只想盡快回家", "後悔選擇商務艙"],
                "answer": 1,
                "explain": "dramatic scenery and diverse culture were worth the long flight。",
            },
        ],
    },
    15: {
        "vocab": [
            {"word": "negotiation", "meaning": "談判", "example": "Two companies entered into a negotiation for an alliance."},
            {"word": "alliance", "meaning": "聯盟", "example": "They finalized a contract for a new alliance."},
            {"word": "compromise", "meaning": "妥協", "example": "The proposal included a compromise on pricing."},
            {"word": "stipulation", "meaning": "規定；條款", "example": "There was a clear stipulation regarding confidentiality."},
            {"word": "objection", "meaning": "反對", "example": "One side raised an objection during the discussion."},
            {"word": "terminate", "meaning": "終止", "example": "They threatened to terminate the agreement."},
            {"word": "settlement", "meaning": "和解；協議結果", "example": "The teams reached a settlement after several hours."},
            {"word": "renew", "meaning": "續約；更新", "example": "They agreed to renew the contract."},
            {"word": "modify", "meaning": "修改", "example": "They modified the original bid to reflect new conditions."},
            {"word": "collaboration", "meaning": "合作", "example": "The process built a foundation for future collaboration."},
            {"word": "expire", "meaning": "到期", "example": "The negotiation would expire soon without a signature."},
            {"word": "bid", "meaning": "出價；投標", "example": "They modified the original bid after talks."},
            {"word": "foundation", "meaning": "基礎", "example": "Trust was the foundation of the deal."},
        ],
        "questions": [
            {
                "q": "提案中包含哪些要素？",
                "choices": ["只有口頭承諾", "條款、價格妥協與機密性規定", "立即終止所有合作", "不需簽名"],
                "answer": 1,
                "explain": "included terms, compromise on pricing, and confidentiality stipulation。",
            },
            {
                "q": "談判中一方提出反對後威脅做什麼？",
                "choices": ["提高報價", "若衝突未解決就終止協議", "立刻續約", "公開所有機密"],
                "answer": 1,
                "explain": "threatened to terminate the agreement if conflict unresolved。",
            },
            {
                "q": "雙方最終達成什麼結果？",
                "choices": ["談判破裂", "達成和解、續約，並縮小專案範圍、修改出價", "無限期延後", "交給法院判決"],
                "answer": 1,
                "explain": "reached settlement, renew contract, narrow scope, modify bid。",
            },
            {
                "q": "“stipulation” 意思最接近？",
                "choices": ["建議", "規定／條款", "謠言", "折扣"],
                "answer": 1,
                "explain": "stipulation regarding confidentiality 指明確規定。",
            },
            {
                "q": "主管對聯盟的看法是？",
                "choices": ["會削弱市場地位", "將強化他們在市場中的地位", "毫無未來價值", "只是短期宣傳"],
                "answer": 1,
                "explain": "director believed the alliance would strengthen their market position。",
            },
        ],
    },
    16: {
        "vocab": [
            {"word": "distribution", "meaning": "配銷；流通", "example": "The trend would affect the distribution of books."},
            {"word": "supplier", "meaning": "供應商", "example": "The client asked the supplier for a checklist."},
            {"word": "inventory", "meaning": "庫存", "example": "Confirm the inventory before finalizing the order."},
            {"word": "invoice", "meaning": "發票", "example": "The invoice would be sent shortly."},
            {"word": "dealer", "meaning": "經銷商", "example": "The dealer offered a discount on bulk purchases."},
            {"word": "bulk", "meaning": "大宗；大量", "example": "Discounts were available on bulk purchases."},
            {"word": "clientele", "meaning": "顧客群", "example": "Assure the clientele of satisfactory service."},
            {"word": "acquisition", "meaning": "取得；收購", "example": "Acquisition of new titles would enhance the rating."},
            {"word": "acclaim", "meaning": "讚揚", "example": "The market would acclaim the collection."},
            {"word": "consignment", "meaning": "寄售", "example": "The consignment agreement would be finalized soon."},
            {"word": "encompass", "meaning": "涵蓋", "example": "The publisher had encompassed all major regions."},
            {"word": "affordability", "meaning": "可負擔性", "example": "The strategy would improve affordability."},
            {"word": "commodity", "meaning": "商品", "example": "The commodity was quoted at a competitive price."},
        ],
        "questions": [
            {
                "q": "客戶在訂單敲定前要求供應商做什麼？",
                "choices": ["提高售價", "提供詳細核對清單並確認庫存", "取消折扣", "停止配銷雜誌"],
                "answer": 1,
                "explain": "provide a detailed checklist and confirm inventory。",
            },
            {
                "q": "關於庫存與折扣，經理說了什麼？",
                "choices": ["庫存充足且無折扣", "大量採購有折扣，但庫存暫時短缺", "完全無法供貨", "只接受現金"],
                "answer": 1,
                "explain": "discount on bulk purchases；stock temporarily short。",
            },
            {
                "q": "團隊決定如何把產品送到零售商？",
                "choices": ["只靠單一門市", "透過商業網路分發並保證滿意服務", "全部出口海外", "停止供應"],
                "answer": 1,
                "explain": "distribute through a commercial network and assure satisfactory service。",
            },
            {
                "q": "“consignment” 在文中指？",
                "choices": ["解雇", "寄售協議", "廣告文案", "印刷錯誤"],
                "answer": 1,
                "explain": "consignment agreement 指寄售協議。",
            },
            {
                "q": "本週末出版社對策略的信心來自什麼？",
                "choices": ["已涵蓋主要地區，預期提升可負擔性並強化夥伴關係", "銷售趨勢結束", "庫存永久短缺", "評分下降"],
                "answer": 0,
                "explain": "encompassed major regions；improve affordability and strengthen partnerships。",
            },
        ],
    },
    17: {
        "vocab": [
            {"word": "cargo", "meaning": "貨物", "example": "They arranged to ship a large cargo of fresh meat."},
            {"word": "crate", "meaning": "木箱", "example": "The goods were packed in a wooden crate."},
            {"word": "parcel", "meaning": "包裹", "example": "He planned to deliver the parcel by mail."},
            {"word": "fragile", "meaning": "易碎的", "example": "Some items were fragile and needed careful handling."},
            {"word": "perishable", "meaning": "易腐壞的", "example": "Perishable goods were stored in a cold facility."},
            {"word": "courier", "meaning": "快遞；承運人", "example": "The courier ensured the shipment was handled adequately."},
            {"word": "affix", "meaning": "貼上；附上", "example": "The recipient was asked to affix a signature."},
            {"word": "warehouse", "meaning": "倉庫", "example": "The warehouse processed all correspondence."},
            {"word": "correspondence", "meaning": "通信文件", "example": "All shipping correspondence was processed by evening."},
            {"word": "detached", "meaning": "拆下；分離", "example": "Workers detached the envelope from each package."},
            {"word": "adequately", "meaning": "充分地；妥善地", "example": "The shipment was handled adequately."},
            {"word": "oblige", "meaning": "滿足……的要求；使感激", "example": "Handle each step correctly to oblige the client."},
            {"word": "shipment", "meaning": "出貨；運送的貨物", "example": "The courier checked the shipment before departure."},
        ],
        "questions": [
            {
                "q": "肉品貨物如何存放以控制溫度？",
                "choices": ["放在室外陽光下", "裝入木箱並存放於冷藏設施", "直接放上車不包裝", "浸泡在水中"],
                "answer": 1,
                "explain": "packed in a wooden crate and stored in a cold facility。",
            },
            {
                "q": "為何快遞特別謹慎處理這批貨物？",
                "choices": ["因為全部免費", "因為部分物品易碎且易腐壞", "因為沒有簽名需求", "因為路線最短"],
                "answer": 1,
                "explain": "some items were fragile and perishable。",
            },
            {
                "q": "代理機構要求收件人做什麼？",
                "choices": ["拒絕取件", "貼上／附上簽名", "拆開所有木箱後再簽名", "改送到公園"],
                "answer": 1,
                "explain": "asked the recipient to affix a signature。",
            },
            {
                "q": "“perishable” 意思最接近？",
                "choices": ["永不損壞", "易腐壞的", "金屬製的", "超重的"],
                "answer": 1,
                "explain": "perishable 指容易腐壞變質。",
            },
            {
                "q": "經理強調正確處理每個步驟的目的是？",
                "choices": ["增加延誤", "避免送錯並讓客戶滿意", "減少通信文件", "取消停車證"],
                "answer": 1,
                "explain": "avoid incorrect delivery and oblige the client。",
            },
        ],
    },
    18: {
        "vocab": [
            {"word": "buffet", "meaning": "自助餐", "example": "A guest took a bite of the buffet dish."},
            {"word": "cafeteria", "meaning": "自助餐廳", "example": "She walked into the cafeteria for cereal."},
            {"word": "recipe", "meaning": "食譜", "example": "He looked for a cookbook recipe idea."},
            {"word": "blend", "meaning": "混合", "example": "He blended clean, fresh ingredients carefully."},
            {"word": "compensate", "meaning": "補償", "example": "Staff would compensate with a complimentary dish."},
            {"word": "complimentary", "meaning": "免費贈送的", "example": "Guests received a complimentary dish from the chef."},
            {"word": "accommodate", "meaning": "容納；配合", "example": "The flavor was stored to accommodate a reception."},
            {"word": "refreshments", "meaning": "茶點；點心飲料", "example": "The team arranged refreshments in advance."},
            {"word": "caterer", "meaning": "外燴業者", "example": "They asked the caterer to handle the reservation."},
            {"word": "cuisine", "meaning": "烹飪；菜餚", "example": "By evening, the cuisine followed a set sequence."},
            {"word": "amenity", "meaning": "便利設施；舒適服務", "example": "Every amenity was designed to ease discomfort."},
            {"word": "extensive", "meaning": "廣泛的；豐富的", "example": "The menu was extensive and required prior approval."},
            {"word": "reservation", "meaning": "預約", "example": "The caterer made the entire reservation."},
        ],
        "questions": [
            {
                "q": "主廚準備海鮮辣味料理時特別小心什麼？",
                "choices": ["不要濺出打發鮮奶油", "不要使用大蒜", "不要試味道", "不要洗碗"],
                "answer": 0,
                "explain": "careful not to spill the whipped cream while blending。",
            },
            {
                "q": "賓客在獲得招待菜前必須先做什麼？",
                "choices": ["離開餐廳", "辦理入住登記（check in）", "自備食材", "取消預約"],
                "answer": 1,
                "explain": "Guests were asked to check in before complimentary dish。",
            },
            {
                "q": "團隊事先請外燴業者處理什麼？",
                "choices": ["整場預約的餐飲", "只洗碗", "只送快遞", "關閉餐廳"],
                "answer": 0,
                "explain": "asked the caterer to make the entire reservation。",
            },
            {
                "q": "“complimentary” 在文中意思是？",
                "choices": ["付費的", "免費贈送的", "批評的", "辛辣的"],
                "answer": 1,
                "explain": "complimentary dish 指免費招待的菜餚。",
            },
            {
                "q": "文末提到設施與服務的設計目的是？",
                "choices": ["增加不便", "減輕不便並照顧賓客物品等需求", "縮短菜單", "取消茶點"],
                "answer": 1,
                "explain": "amenities were designed to ease discomfort，包括照顧 belongings。",
            },
        ],
    },
    19: {
        "vocab": [
            {"word": "revenue", "meaning": "營收", "example": "The revenue projection showed a substantial increase."},
            {"word": "projection", "meaning": "預測", "example": "Management will revise the annual projection later."},
            {"word": "substantial", "meaning": "大幅度的；可觀的", "example": "There was a substantial increase in revenue."},
            {"word": "markedly", "meaning": "明顯地", "example": "Some figures declined markedly."},
            {"word": "anticipate", "meaning": "預期", "example": "The analyst anticipated a shift in fee structure."},
            {"word": "estimate", "meaning": "估計", "example": "An estimate shift could affect production sales."},
            {"word": "exceed", "meaning": "超過", "example": "Recent figures exceeded expectations."},
            {"word": "incur", "meaning": "招致；承擔（成本）", "example": "Incurred costs were offset by rising profit."},
            {"word": "offset", "meaning": "抵銷", "example": "The overseas decline was offset by domestic revenue."},
            {"word": "reliant", "meaning": "依賴的", "example": "The company remained reliant on exports."},
            {"word": "domestic", "meaning": "國內的", "example": "Domestic revenue increased by quarter end."},
            {"word": "decline", "meaning": "下降", "example": "There was a decline in overseas orders."},
            {"word": "steady", "meaning": "穩定的", "example": "Whole growth figures remained steady."},
        ],
        "questions": [
            {
                "q": "營收預測顯示什麼情況？",
                "choices": ["全面崩潰", "大幅增加，但部分數字明顯下滑", "完全沒有變化", "只談租金"],
                "answer": 1,
                "explain": "substantial increase, although some figures declined markedly。",
            },
            {
                "q": "分析師預期什麼可能影響產銷？",
                "choices": ["天氣報告", "費用結構的轉變", "辦公室裝潢", "員工午餐"],
                "answer": 1,
                "explain": "anticipated an estimate shift in fee structure affecting sales。",
            },
            {
                "q": "本季結束時，海外訂單下滑如何被平衡？",
                "choices": ["無法平衡", "被國內營收增加抵銷", "靠提高租金", "靠減少出口依賴卻無成果"],
                "answer": 1,
                "explain": "decline in overseas orders was offset by domestic revenue increase。",
            },
            {
                "q": "“offset” 意思最接近？",
                "choices": ["加倍", "抵銷", "忽略", "誇大"],
                "answer": 1,
                "explain": "offset 表示抵銷、補償。",
            },
            {
                "q": "管理層在修正年度預測前會先做什麼？",
                "choices": ["立刻公布最終數字", "預期需求進一步轉變", "停止檢視出口", "取消代表報告"],
                "answer": 1,
                "explain": "will anticipate further shift in demand before revising projection。",
            },
        ],
    },
    20: {
        "vocab": [
            {"word": "abundant", "meaning": "充足的", "example": "Abundant funds allowed the department to hold a contest."},
            {"word": "committee", "meaning": "委員會", "example": "A powerful committee reviewed the advisor's plan."},
            {"word": "funding", "meaning": "資金；資助", "example": "They decided to double funding for next year."},
            {"word": "audit", "meaning": "審計", "example": "The audit confirmed the deficit was substantially reduced."},
            {"word": "curtail", "meaning": "縮減；削減", "example": "Financial curtail of the deficit showed progress."},
            {"word": "deficit", "meaning": "赤字", "example": "The financial deficit was substantially reduced."},
            {"word": "reimburse", "meaning": "報銷；償還", "example": "Staff will reimburse and allocate funds after approval."},
            {"word": "allocate", "meaning": "分配", "example": "Allocate adequate total funds once approved."},
            {"word": "fiscal", "meaning": "財政的；會計年度的", "example": "Turnover figures were reviewed by fiscal year end."},
            {"word": "inflation", "meaning": "通膨", "example": "Inflation pushed departments to review fiscal planning."},
            {"word": "proceeds", "meaning": "收益", "example": "The committee reviewed capability to manage proceeds."},
            {"word": "temporary", "meaning": "暫時的", "example": "Some spending cuts were called temporary."},
            {"word": "turnover", "meaning": "營業額", "example": "Turnover figures were reviewed by the finance team."},
        ],
        "questions": [
            {
                "q": "預算受到質疑後，委員會決定做什麼？",
                "choices": ["取消所有計畫", "將資金加倍以產生更多成果", "停止審計", "忽略顧問建議"],
                "answer": 1,
                "explain": "decided to double funding to generate more results。",
            },
            {
                "q": "審計確認了什麼？",
                "choices": ["赤字大幅增加", "財務赤字經緊縮後已大幅減少", "完全沒有預算", "通膨消失"],
                "answer": 1,
                "explain": "audit confirmed the financial curtail deficit was substantially reduced。",
            },
            {
                "q": "員工何時會報銷並分配資金？",
                "choices": ["永遠不會", "檢查員核准偏好的季度計畫之後", "比賽開始前隨便分配", "通膨結束後才討論"],
                "answer": 1,
                "explain": "once the inspector approves the preferred quarter plan。",
            },
            {
                "q": "“allocate” 意思最接近？",
                "choices": ["浪費", "分配", "隱藏", "借出私人款"],
                "answer": 1,
                "explain": "allocate funds 表示分配資金。",
            },
            {
                "q": "通膨對各部门造成什麼影響？",
                "choices": ["不再審查預算", "更頻繁地審查財政規劃", "自動增加所有經費", "取消委員會"],
                "answer": 1,
                "explain": "Inflation pushed departments to review fiscal planning more frequently。",
            },
        ],
    },
    21: {
        "vocab": [
            {"word": "critic", "meaning": "評論者；批評者", "example": "The branch's critic warned against repeating past mistakes."},
            {"word": "partnership", "meaning": "合夥關係", "example": "Staff prepared equipment for the new partnership."},
            {"word": "foresee", "meaning": "預見", "example": "Few could foresee the expansion."},
            {"word": "relocate", "meaning": "搬遷", "example": "The firm plans to relocate away from a strong competitor."},
            {"word": "asset", "meaning": "資產", "example": "Relocation would help protect its asset."},
            {"word": "dedicated", "meaning": "專注奉獻的", "example": "Employees contribute in a dedicated way."},
            {"word": "considerable", "meaning": "相當多的；可觀的", "example": "Be careful not to misplace considerable files."},
            {"word": "merge", "meaning": "合併", "example": "They will select a partner to merge with."},
            {"word": "persist", "meaning": "持續", "example": "Independent growth must persist after the merger."},
            {"word": "improbable", "meaning": "不太可能的", "example": "It seemed improbable to gain every advantage at once."},
            {"word": "expansion", "meaning": "擴張", "example": "Few could foresee the expansion plan."},
            {"word": "competitor", "meaning": "競爭者", "example": "They relocated away from a strong competitor."},
            {"word": "edge", "meaning": "優勢", "example": "Gaining an edge this quarter seemed difficult."},
        ],
        "questions": [
            {
                "q": "評論家對分公司的批評重點是什麼？",
                "choices": ["過度外向", "可能重複過去錯誤且過於內向保守", "擴張太快", "檔案管理完美"],
                "answer": 1,
                "explain": "repeating mistakes... looking too far inward。",
            },
            {
                "q": "公司計畫如何保護資產？",
                "choices": ["靠近競爭對手", "搬遷以遠離強勁競爭對手", "丟棄檔案", "停止成長"],
                "answer": 1,
                "explain": "plans to relocate away from a strong competitor, protecting its asset。",
            },
            {
                "q": "關於年底併購，文中暗示什麼？",
                "choices": ["合併後就不需獨立成長", "即使合併，持續且獨立的成長仍很重要", "不可能選到夥伴", "銷售已經停止"],
                "answer": 1,
                "explain": "merge... though this implies vital persist independent growth。",
            },
            {
                "q": "“foresee” 意思最接近？",
                "choices": ["忽略", "預見", "阻止", "慶祝"],
                "answer": 1,
                "explain": "few could foresee the expansion 表示很少人預見到擴張。",
            },
            {
                "q": "員工在新合夥準備中被要求注意什麼？",
                "choices": ["隨意放置檔案", "以專注態度貢獻，小心不遺失大量檔案", "拒絕抬設備", "停止銷售"],
                "answer": 1,
                "explain": "contribute dedicatedly；not misplace considerable files。",
            },
        ],
    },
    22: {
        "vocab": [
            {"word": "handout", "meaning": "講義；發放資料", "example": "The guest speaker passed out a handout."},
            {"word": "agenda", "meaning": "議程", "example": "The agenda was set to convene the team."},
            {"word": "convene", "meaning": "召集；召開", "example": "The agenda was set to convene the team."},
            {"word": "refute", "meaning": "反駁", "example": "One member tried to refute the agenda."},
            {"word": "unanimous", "meaning": "一致的", "example": "Reaching a unanimous decision required consensus."},
            {"word": "consensus", "meaning": "共識", "example": "Someone needed to build consensus among the group."},
            {"word": "defer", "meaning": "延後", "example": "Otherwise they would defer the vote."},
            {"word": "reschedule", "meaning": "改期", "example": "Usually they reschedule meetings when needed."},
            {"word": "preside", "meaning": "主持", "example": "Someone should preside over the meeting constructively."},
            {"word": "constructive", "meaning": "建設性的", "example": "It would be constructive to ignore irrelevant issues."},
            {"word": "coordination", "meaning": "協調", "example": "Refuting the agenda caused a lack of coordination."},
            {"word": "debate", "meaning": "辯論", "example": "The event included lively conversation and debate."},
            {"word": "approve", "meaning": "批准", "example": "The board will approve the enclosed record suggestion."},
        ],
        "questions": [
            {
                "q": "客座演講者在演說前做了什麼？",
                "choices": ["取消會議", "發放講義並請員工掃視筆記、握手", "要求立刻投票", "關掉會議室"],
                "answer": 1,
                "explain": "passed out a handout；ask staff to scan notes and shake hands。",
            },
            {
                "q": "有成員試圖反駁議程造成什麼結果？",
                "choices": ["立刻一致通過", "協調出現問題", "會議自動結束", "董事會離席慶祝"],
                "answer": 1,
                "explain": "causing a lack of coordination。",
            },
            {
                "q": "若無法建立共識，會議可能怎麼做？",
                "choices": ["強制通過違法決議", "延後投票", "刪除所有紀錄", "換掉整棟大樓"],
                "answer": 1,
                "explain": "or else defer the vote。",
            },
            {
                "q": "“unanimous” 意思最接近？",
                "choices": ["分歧的", "全體一致的", "秘密的", "延遲的"],
                "answer": 1,
                "explain": "unanimous decision 指一致決議。",
            },
            {
                "q": "文末認為什麼做法更具建設性？",
                "choices": ["讓無關限制性議題主導會議", "有人主持會議並忽略無關限制性議題", "完全不批准紀錄", "禁止辯論"],
                "answer": 1,
                "explain": "constructive for someone to preside... ignoring irrelevant constraint issues。",
            },
        ],
    },
    23: {
        "vocab": [
            {"word": "ceremony", "meaning": "典禮", "example": "The award ceremony required advance registration."},
            {"word": "register", "meaning": "登記；註冊", "example": "Each participant had to register in advance."},
            {"word": "seminar", "meaning": "研討會", "example": "Employees planned to attend the management seminar."},
            {"word": "lecture", "meaning": "講座", "example": "The learning center would host a lecture for all staff."},
            {"word": "enroll", "meaning": "報名；註冊入學", "example": "The organizer wanted to enroll everyone in the conference."},
            {"word": "honor", "meaning": "表揚；致敬", "example": "A function would honor outstanding contributions."},
            {"word": "emphasize", "meaning": "強調", "example": "The schedule would emphasize teamwork."},
            {"word": "tentative", "meaning": "暫定的", "example": "They regarded the tentative welcome as a positive sign."},
            {"word": "commence", "meaning": "開始", "example": "The objective was to commence the ceremony with excitement."},
            {"word": "reimbursement", "meaning": "報銷；償付", "example": "Travel expenses would receive reimbursement."},
            {"word": "recognition", "meaning": "認可；表揚", "example": "Staff believed their hard work earned recognition."},
            {"word": "participation", "meaning": "參與", "example": "The purpose was to encourage participation."},
            {"word": "outstanding", "meaning": "傑出的", "example": "The event honored outstanding contributions."},
        ],
        "questions": [
            {
                "q": "頒獎典禮申請的要求是？",
                "choices": ["當天臨時報到即可", "每位參與者事先登記", "只需口頭通知朋友", "不必報名"],
                "answer": 1,
                "explain": "required each participant to register in advance。",
            },
            {
                "q": "主辦者說明活動目的是？",
                "choices": ["減少加班", "鼓勵參與並讓大家報名年度會議", "取消表揚", "只發放飲料"],
                "answer": 1,
                "explain": "encourage participation and enroll everyone in the annual conference。",
            },
            {
                "q": "行程中包含什麼表揚相關安排？",
                "choices": ["沒有表揚環節", "表揚傑出貢獻並強調團隊合作的聚會", "只討論裁員", "強制取消加薪"],
                "answer": 1,
                "explain": "function to honor outstanding contributions and emphasize teamwork。",
            },
            {
                "q": "“commence” 意思最接近？",
                "choices": ["結束", "開始", "延後", "批評"],
                "answer": 1,
                "explain": "commence the ceremony 表示開始典禮。",
            },
            {
                "q": "夜晚結束時宣布了什麼？",
                "choices": ["只宣布放假", "參賽獎金與加薪，員工覺得努力獲認可", "取消研討會", "停止報銷差旅"],
                "answer": 1,
                "explain": "entry bonus and salary increase were announced；earned recognition。",
            },
        ],
    },
    24: {
        "vocab": [
            {"word": "anniversary", "meaning": "週年紀念", "example": "He accepted an award at the anniversary celebration."},
            {"word": "appraisal", "meaning": "評鑑；考核", "example": "He was appointed after a positive appraisal."},
            {"word": "appointed", "meaning": "被任命的", "example": "He was appointed to a new role."},
            {"word": "promote", "meaning": "晉升；升遷", "example": "Management decided to promote a skilled worker."},
            {"word": "resign", "meaning": "辭職", "example": "He considered whether to resign his role."},
            {"word": "safeguard", "meaning": "防護措施", "example": "Safeguards were in place to prevent conflicts."},
            {"word": "competent", "meaning": "能幹的；勝任的", "example": "The board promoted the most competent candidate."},
            {"word": "unanimous", "meaning": "一致同意的", "example": "The board reached a unanimous decision."},
            {"word": "mandatory", "meaning": "強制性的", "example": "The award recognized mandatory competent performance."},
            {"word": "characteristic", "meaning": "特質；特徵", "example": "He reviewed his characteristic helping contributions."},
            {"word": "preference", "meaning": "偏好；優先選擇", "example": "The team suggested a new preference after evaluation."},
            {"word": "radically", "meaning": "徹底地；極端地", "example": "His radically exceptional work impressed management."},
            {"word": "conflict", "meaning": "衝突", "example": "Safeguards helped prevent conflicts over differing views."},
        ],
        "questions": [
            {
                "q": "他在週年慶祝活動領獎後還發生什麼事？",
                "choices": ["公司關閉", "有人被解僱，而他需確認新職稱", "他立刻辭職成功", "董事會解散"],
                "answer": 1,
                "explain": "someone was fired；he confirmed his new job title。",
            },
            {
                "q": "他對自己職位的態度是？",
                "choices": ["完全絕望", "仍抱希望，但也考慮是否辭職", "拒絕約談", "要求立即解雇主管"],
                "answer": 1,
                "explain": "remained hopeful... though he considered whether to resign。",
            },
            {
                "q": "正面評鑑之後管理層做了什麼？",
                "choices": ["降職", "任命並晉升這位熟練員工", "忽略表現", "取消所有獎項"],
                "answer": 1,
                "explain": "appointed after positive appraisal；promote a skilled worker。",
            },
            {
                "q": "“appraisal” 在人事語境中最接近？",
                "choices": ["聚餐", "績效評鑑", "出差", "廣告"],
                "answer": 1,
                "explain": "positive appraisal 指正面的考核／評鑑。",
            },
            {
                "q": "董事會最後如何決定晉升？",
                "choices": ["抽籤決定", "一致決定晉升最有能力的候選人", "由批評者決定", "隨機輪調"],
                "answer": 1,
                "explain": "unanimous decision to promote the most competent candidate。",
            },
        ],
    },
    25: {
        "vocab": [
            {"word": "crosswalk", "meaning": "行人穿越道", "example": "He used the crosswalk near free parking."},
            {"word": "highway", "meaning": "高速公路", "example": "He faced heavy traffic on the highway."},
            {"word": "subway", "meaning": "地鐵", "example": "He checked the subway station for the tour bus."},
            {"word": "congestion", "meaning": "壅塞", "example": "Traffic congestion forced drivers to take a detour."},
            {"word": "alleviate", "meaning": "減輕；緩和", "example": "Drivers tried to alleviate delays by taking a detour."},
            {"word": "detour", "meaning": "繞道", "example": "Taking a detour helped save fuel."},
            {"word": "malfunction", "meaning": "故障", "example": "A malfunction meant the car lacked a valid permit."},
            {"word": "permit", "meaning": "許可證", "example": "The car lacked a valid permit for transportation."},
            {"word": "intersection", "meaning": "交叉路口", "example": "The route helped obtain access to a designated intersection."},
            {"word": "commute", "meaning": "通勤", "example": "By the end of the commute, the car was ready."},
            {"word": "mechanic", "meaning": "技工；修車師傅", "example": "He had to trust the mechanic before driving."},
            {"word": "equipped", "meaning": "配備齊全的", "example": "The car was equipped for a long downtown trip."},
            {"word": "rental", "meaning": "租賃", "example": "He called a cab instead of using car rental."},
        ],
        "questions": [
            {
                "q": "在公車站時，他選擇什麼交通方式？",
                "choices": ["租車服務", "叫計程車", "步行回家放棄行程", "搭船"],
                "answer": 1,
                "explain": "called a cab instead of using the car rental service。",
            },
            {
                "q": "交通壅塞時駕駛人如何因應？",
                "choices": ["停在原地等候整天", "繞道以緩解延誤並節省燃料", "關閉引擎離開車輛", "忽略所有號誌"],
                "answer": 1,
                "explain": "alleviate delays by taking a detour to save fuel。",
            },
            {
                "q": "故障造成什麼後果？",
                "choices": ["獲得免費加油", "車輛缺乏有效運輸許可，錯失重要機會", "立刻到達市中心", "交通完全暢通"],
                "answer": 1,
                "explain": "lacked a valid permit... missing an important opportunity。",
            },
            {
                "q": "“congestion” 意思最接近？",
                "choices": ["順暢", "壅塞", "免費", "許可"],
                "answer": 1,
                "explain": "traffic congestion 指交通壅塞。",
            },
            {
                "q": "通勤結束前他還必須做什麼才能出發？",
                "choices": ["丟棄車輛", "支付費用並信任技師", "取消所有替代路線", "關閉車庫永久"],
                "answer": 1,
                "explain": "pay an expense and trust the mechanic before he could drive。",
            },
        ],
    },
    26: {
        "vocab": [
            {"word": "balance", "meaning": "餘額", "example": "He wanted to check his balance while opening an account."},
            {"word": "automatic", "meaning": "自動的", "example": "He planned to use automatic payment."},
            {"word": "deposit", "meaning": "存款", "example": "The balance was too low after the last deposit."},
            {"word": "delinquent", "meaning": "逾期未付的", "example": "The bank sent a delinquent notice about the account."},
            {"word": "overdue", "meaning": "逾期的", "example": "The notice concerned an overdue account."},
            {"word": "withdrawal", "meaning": "提款", "example": "The investigation reviewed an amount withdrawal."},
            {"word": "statement", "meaning": "對帳單；明細", "example": "An investigation into the account statement began."},
            {"word": "certificate", "meaning": "證明文件", "example": "She needed a certificate documenting her spending."},
            {"word": "interest", "meaning": "利息", "example": "Customers complained about interest rates and fees."},
            {"word": "mortgage", "meaning": "房貸", "example": "Staff hoped to convert discounted loan and mortgage fees."},
            {"word": "payable", "meaning": "應付的", "example": "Personal fees remained payable at month end."},
            {"word": "reject", "meaning": "拒絕", "example": "The bank decided to reject the relation application."},
            {"word": "identification", "meaning": "身分核實；身分證明", "example": "Identification revealed dissatisfaction with rates."},
        ],
        "questions": [
            {
                "q": "他一開始想同時完成哪兩件事？",
                "choices": ["關閉帳戶並提領全部現金", "開戶並查看餘額，同時使用自動付款", "申請信用卡卻不交文件", "只看新聞不辦業務"],
                "answer": 1,
                "explain": "open an account... checking his balance... using automatic payment。",
            },
            {
                "q": "銀行為何寄出逾期通知？",
                "choices": ["餘額過高", "帳戶逾期，且上次存款後餘額過低", "客戶拒絕利息", "職員弄丟硬幣"],
                "answer": 1,
                "explain": "delinquent notice about overdue account；balance too low after deposit。",
            },
            {
                "q": "對帳單調查顯示什麼？",
                "choices": ["提款早已處理完畢", "提款金額先前已到期卻尚未處理", "完全沒有交易", "利率全部為零"],
                "answer": 1,
                "explain": "withdrawal was previously due but not yet processed。",
            },
            {
                "q": "“delinquent” 在帳戶語境中最接近？",
                "choices": ["優良的", "逾期未付的", "新建的", "保密的"],
                "answer": 1,
                "explain": "delinquent notice 指逾期未付相關通知。",
            },
            {
                "q": "月底身分核實後銀行採取什麼行動？",
                "choices": ["立刻批准所有申請", "因對利率不滿等因素拒絕該關聯申請", "取消所有手續費且無條件放貸", "停止自動付款系統永久"],
                "answer": 1,
                "explain": "dissatisfaction with interest rates... leading the bank to reject the relation。",
            },
        ],
    },
    27: {
        "vocab": [
            {"word": "investment", "meaning": "投資", "example": "He worried it might be a fake joint investment."},
            {"word": "mentor", "meaning": "導師；顧問", "example": "He chose to listen to his mentor on the network."},
            {"word": "lucrative", "meaning": "有利可圖的", "example": "The investment proved lucrative."},
            {"word": "foreseeable", "meaning": "可預見的", "example": "It was possible to secure a foreseeable gain."},
            {"word": "innate", "meaning": "天生的；固有的", "example": "Gains came thanks to innate market timing."},
            {"word": "lease", "meaning": "租約", "example": "Buying property required a formal lease."},
            {"word": "sponsor", "meaning": "贊助者", "example": "A sponsor agreed to propose support."},
            {"word": "portfolio", "meaning": "投資組合", "example": "Cautious insight guided the portfolio decisions."},
            {"word": "speculation", "meaning": "投機；臆測", "example": "Possible speculation guided the fund manager."},
            {"word": "shareholder", "meaning": "股東", "example": "He convinced a shareholder to trust the outlook."},
            {"word": "depreciation", "meaning": "貶值；折舊", "example": "Bond depreciation worried conservative investors."},
            {"word": "yield", "meaning": "收益率", "example": "Unprecedented yield figures concerned investors."},
            {"word": "stability", "meaning": "穩定性", "example": "He promoted a positive outlook for market stability."},
        ],
        "questions": [
            {
                "q": "他擔心合資項目可能有什麼問題？",
                "choices": ["報酬太高", "可能是假的合資投資", "沒有導師", "租車太貴"],
                "answer": 1,
                "explain": "worried it might be a fake joint investment。",
            },
            {
                "q": "這項投資後來被證明如何？",
                "choices": ["完全虧損", "有利可圖，並可能取得可預見獲利", "無法交易", "只能買債券"],
                "answer": 1,
                "explain": "proved lucrative... foreseeable gain thanks to market timing。",
            },
            {
                "q": "代表客戶購屋需要什麼？",
                "choices": ["口頭承諾即可", "正式租約，並有贊助者支持", "取消投資組合", "忽略法律文件"],
                "answer": 1,
                "explain": "required a formal lease, backed by a sponsor。",
            },
            {
                "q": "“lucrative” 意思最接近？",
                "choices": ["虧損的", "有利可圖的", "違法的", "短暫的"],
                "answer": 1,
                "explain": "lucrative investment 指有利可圖的投資。",
            },
            {
                "q": "年底什麼情況讓保守型投資人擔憂？",
                "choices": ["股價全部凍結", "債券貶值與前所未有的收益率數字", "沒有任何市場消息", "租約全部作廢"],
                "answer": 1,
                "explain": "bond depreciation... unprecedented yield figures worried conservative investors。",
            },
        ],
    },
    28: {
        "vocab": [
            {"word": "remodeling", "meaning": "改建；整修", "example": "During the remodeling, workers repaired the rooftop."},
            {"word": "veranda", "meaning": "陽台；走廊", "example": "They cleaned the water tank on the veranda."},
            {"word": "dwell", "meaning": "居住", "example": "He set up his desktop where he chose to dwell."},
            {"word": "inhabit", "meaning": "居住於", "example": "Residents who inhabit this urban area appreciate the light."},
            {"word": "furnished", "meaning": "附家具的", "example": "The furnished residence felt spacious."},
            {"word": "unoccupied", "meaning": "未被佔用的；空著的", "example": "New drapes covered the once unoccupied room."},
            {"word": "renovation", "meaning": "翻修", "example": "The room looked better after renovation."},
            {"word": "contractor", "meaning": "承包商", "example": "The contractor plans to develop and maintain the site."},
            {"word": "adjacent", "meaning": "鄰近的", "example": "The property is adjacent to the park."},
            {"word": "densely", "meaning": "密集地", "example": "The area is densely populated."},
            {"word": "utility", "meaning": "公共設施；公用事業", "example": "The property would have modern utility connections."},
            {"word": "restore", "meaning": "恢復；修復", "example": "Staff will arrange the location and restore it."},
            {"word": "abandon", "meaning": "放棄", "example": "There are reasons to abandon the old plan."},
        ],
        "questions": [
            {
                "q": "改建期間工人做了哪些事？",
                "choices": ["只油漆牆壁", "修屋頂、固定繩索並清理陽台水槽", "拆除整個社區", "搬空所有家具後離職"],
                "answer": 1,
                "explain": "repaired rooftop, secured rope, cleaned water tank on veranda。",
            },
            {
                "q": "關於翻修後的住宅，文中如何描述？",
                "choices": ["更狹窄", "附家具且寬敞，空房也裝了新窗簾", "無法居住", "沒有照明"],
                "answer": 1,
                "explain": "furnished residence felt spacious；drapes covered unoccupied room。",
            },
            {
                "q": "為何預期工程可能延遲是合理的？",
                "choices": ["完全沒有監督", "社區建設維修正定期受監督", "承包商消失", "公園關閉"],
                "answer": 1,
                "explain": "community construction repair was currently regularly monitored。",
            },
            {
                "q": "“adjacent” 意思最接近？",
                "choices": ["遙遠的", "鄰近的", "地下的", "臨時的"],
                "answer": 1,
                "explain": "adjacent to the park 表示緊鄰公園。",
            },
            {
                "q": "專案結束時承包商的計畫是？",
                "choices": ["放棄維護", "開發並維護該地點，即使人口密集", "只建圍欄", "移除所有公共設施"],
                "answer": 1,
                "explain": "plans to develop and maintain the site, even though densely populated。",
            },
        ],
    },
    29: {
        "vocab": [
            {"word": "humid", "meaning": "潮濕的", "example": "The harvest took place in a humid landscape."},
            {"word": "pollution", "meaning": "污染", "example": "He worried about dust, flood, and pollution."},
            {"word": "contamination", "meaning": "污染；沾污", "example": "The source of contamination came from temperature shifts."},
            {"word": "conserve", "meaning": "節約；保育", "example": "Efforts to conserve resources increased recycling."},
            {"word": "dispose", "meaning": "處置；丟棄", "example": "Find better ways to dispose of waste through recycling."},
            {"word": "recycling", "meaning": "回收", "example": "Recycling helps reduce waste in the forecast."},
            {"word": "preserve", "meaning": "保存；保護", "example": "It was ideal to preserve and aid the land."},
            {"word": "inaccessible", "meaning": "無法進入的", "example": "Some areas became inaccessible by season's end."},
            {"word": "emission", "meaning": "排放", "example": "Residents were disturbed by pollutant emission and smog."},
            {"word": "smog", "meaning": "霧霾", "example": "Dense smog worried local residents."},
            {"word": "discharge", "meaning": "排放；放出", "example": "The report covered disaster discharge and resource use."},
            {"word": "forecast", "meaning": "預報", "example": "The forecast may show less waste with better recycling."},
            {"word": "occurrence", "meaning": "發生；事件", "example": "The solution helped prevent further occurrence."},
        ],
        "questions": [
            {
                "q": "污染源被歸因於什麼？",
                "choices": ["圖書館噪音", "南方氣溫轉變造成的異常天氣模式", "過多的回收桶", "洞穴觀光"],
                "answer": 1,
                "explain": "contamination came from southern temperature shift causing unusual weather。",
            },
            {
                "q": "保育資源的努力預期帶來什麼？",
                "choices": ["更多垃圾", "預報顯示更少廢棄物，並透過回收更好處置", "停止所有清理", "增加工廠排放"],
                "answer": 1,
                "explain": "forecast would show less waste and better dispose through recycling。",
            },
            {
                "q": "季末居民受到什麼困擾？",
                "choices": ["天氣過於寒冷而已", "部分地區無法進入，且排放造成濃厚霧霾", "種子生長過快", "完全沒有污染報告"],
                "answer": 1,
                "explain": "areas inaccessible；disturbed by rising pollutant emission dense smog。",
            },
            {
                "q": "“conserve” 意思最接近？",
                "choices": ["浪費", "節約／保育", "排放", "破壞"],
                "answer": 1,
                "explain": "conserve resources 表示節約或保育資源。",
            },
            {
                "q": "報告讓官員擔憂的內容包括？",
                "choices": ["觀光人數增加", "環境洩漏、持續污染、災難性排放與資源消耗", "回收率百分之百", "沙漠完全綠化"],
                "answer": 1,
                "explain": "leak, continually contaminate, disaster discharge, resource report worried officials。",
            },
        ],
    },
    30: {
        "vocab": [
            {"word": "allergic", "meaning": "過敏的", "example": "The allergic patient visited a cosmetic clinic."},
            {"word": "cavity", "meaning": "蛀牙；空洞", "example": "A cavity and cold were diagnosed at the clinic."},
            {"word": "checkup", "meaning": "健康檢查", "example": "He visited a medical facility for a checkup."},
            {"word": "injection", "meaning": "注射", "example": "The doctor prepared an injection for treatment."},
            {"word": "physician", "meaning": "醫師", "example": "The physician prescribed a remedy for his stomachache."},
            {"word": "remedy", "meaning": "療法；藥物", "example": "A remedy was prescribed for overall wellbeing."},
            {"word": "operation", "meaning": "手術", "example": "Healing required a simple operation."},
            {"word": "comprehensive", "meaning": "全面的", "example": "A comprehensive examination eliminated some concerns."},
            {"word": "pharmaceutical", "meaning": "製藥的；藥品的", "example": "Pharmaceutical premiums were part of his coverage."},
            {"word": "prevention", "meaning": "預防", "example": "He joined a prevention program after recovery."},
            {"word": "nutrition", "meaning": "營養", "example": "The doctor induced better nutrition habits."},
            {"word": "susceptibility", "meaning": "易感性；易受影響的程度", "example": "Better coverage may reduce susceptibility to illness."},
            {"word": "transmitted", "meaning": "傳染的；傳遞的", "example": "The exam eliminated easily transmitted reactions."},
        ],
        "questions": [
            {
                "q": "病人在美容診所被診斷出什麼？",
                "choices": ["骨折", "蛀牙與感冒", "只是疲勞", "完全健康"],
                "answer": 1,
                "explain": "a cavity and cold were diagnosed。",
            },
            {
                "q": "醫師為他開立藥物主要針對什麼？",
                "choices": ["視力手術後護理費", "牙痛、胃痛與整體健康", "健身房會籍", "雨衣購買"],
                "answer": 1,
                "explain": "prescribed a remedy for stomachache and overall wellbeing；toothache needed treatment。",
            },
            {
                "q": "全面檢查後建議什麼？",
                "choices": ["停止所有檢查", "定期牙科與飲食檢查", "忽略營養", "取消保險"],
                "answer": 1,
                "explain": "recommended periodic dental and dietary checks。",
            },
            {
                "q": "“susceptibility” 意思最接近？",
                "choices": ["抵抗力極強", "易感性／容易患病的程度", "手術成功率", "保險拒保"],
                "answer": 1,
                "explain": "reduce susceptibility to future illness 指降低易感性。",
            },
            {
                "q": "康復後他採取什麼行動？",
                "choices": ["拒絕預防計畫", "意識到健康匱乏並加入預防計畫，改善營養與保險覆蓋", "停止看醫生", "只做美容療程"],
                "answer": 1,
                "explain": "conscious of health deprivation and joined a prevention program；better nutrition and insurance。",
            },
        ],
    },
}


def to_js_literal(obj) -> str:
    """Serialize Python object to a JS literal with Chinese preserved."""
    return json.dumps(obj, ensure_ascii=False, indent=2)


def build_days(raw: list[dict]) -> list[dict]:
    days: list[dict] = []
    for item in raw:
        day = int(item["day"])
        theme_en, theme_zh = THEMES[day]
        content = DAY_CONTENT[day]
        vocab = content["vocab"]
        questions = content["questions"]

        if not (12 <= len(vocab) <= 15):
            raise ValueError(f"Day {day}: vocab count {len(vocab)} not in 12–15")
        if len(questions) != 5:
            raise ValueError(f"Day {day}: questions count {len(questions)} != 5")
        for i, q in enumerate(questions):
            if len(q["choices"]) != 4:
                raise ValueError(f"Day {day} Q{i}: need 4 choices")
            if not (0 <= q["answer"] <= 3):
                raise ValueError(f"Day {day} Q{i}: answer out of range")

        english = item["english"].strip()
        # Soft check: vocab words should appear in English (case-insensitive root)
        missing = []
        lower_en = english.lower()
        for v in vocab:
            w = v["word"].lower()
            if w not in lower_en and w.rstrip("d") not in lower_en and w.rstrip("s") not in lower_en:
                # allow common morphological variants already handled loosely
                if not any(tok.startswith(w[:4]) for tok in lower_en.split() if len(w) >= 4):
                    missing.append(v["word"])
        if missing:
            # Warn but do not fail — some lemmas differ (boarded/board, etc.)
            print(f"Note day {day}: soft-miss vocab check: {missing}")

        days.append(
            {
                "day": day,
                "phase": phase_for(day),
                "theme": theme_en,
                "themeZh": theme_zh,
                "title": item["title"],
                "english": english,
                "chinese": clean_chinese(item["chinese"]).strip(),
                "vocab": vocab,
                "questions": questions,
            }
        )
    days.sort(key=lambda d: d["day"])
    if len(days) != 30:
        raise ValueError(f"Expected 30 days, got {len(days)}")
    return days


def main() -> None:
    raw = json.loads(SRC.read_text(encoding="utf-8"))
    days = build_days(raw)
    js = "window.TOEIC_DAYS = " + to_js_literal(days) + ";\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(js, encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Days: {len(days)}")
    # Verify Chinese cleanup
    for d in days:
        if "# TOEIC" in d["chinese"]:
            raise SystemExit(f"Leaked header still in day {d['day']}")
    d1 = days[0]
    print("Sample day1 vocab[0]:", json.dumps(d1["vocab"][0], ensure_ascii=False))
    print("Sample day1 questions[0]:", json.dumps(d1["questions"][0], ensure_ascii=False))


if __name__ == "__main__":
    main()
