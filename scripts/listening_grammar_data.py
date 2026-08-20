# -*- coding: utf-8 -*-
"""Listening + grammar enrichment for all 30 TOEIC study days."""

from __future__ import annotations

Q = dict  # typing convenience


def _q(q: str, choices: list[str], answer: int, explain: str) -> dict:
    return {"q": q, "choices": choices, "answer": answer, "explain": explain}


def part_focus_for(day: int) -> str:
    """Weekly listening Part rotation (must match curriculum)."""
    if day <= 7:
        if day == 7:
            return "LC Mixed"
        return "Part 1" if day % 2 == 1 else "Part 2"
    if day <= 14:
        if day == 14:
            return "LC Mixed"
        return "Part 3" if day % 2 == 0 else "Part 4"
    if day <= 22:
        if day == 21:
            return "LC Mixed"
        # Part 3–4 heavy with some Mixed for weak skills
        if day in (15, 17, 20):
            return "Part 3"
        if day in (16, 18, 22):
            return "Part 4"
        return "LC Mixed"  # 19
    # Days 23–30: exam rhythm; Day 28 = LC Mixed (all Mixed)
    return "LC Mixed"


def grammar_focus_for(day: int) -> str:
    week1 = ["詞性", "主謂一致", "介系詞", "連接詞", "時態", "詞性／主謂一致", "介系詞／時態"]
    week2 = ["被動語態", "不定詞／動名詞", "關係代名詞", "條件句", "Part 6 文意", "被動／不定詞", "關係子句／條件句"]
    week3 = ["進階詞彙題", "易混淆字", "正式商務語氣", "長句結構", "進階詞彙／易混淆字", "正式語氣／長句", "綜合商務文法", "長句／詞彙陷阱"]
    week4 = ["綜合錯題型", "陷阱選項", "綜合錯題型", "陷阱選項", "綜合錯題型", "陷阱選項", "綜合錯題型", "陷阱選項"]
    if day <= 7:
        return week1[day - 1]
    if day <= 14:
        return week2[day - 8]
    if day <= 22:
        return week3[day - 15]
    return week4[day - 23]


# ---------------------------------------------------------------------------
# Per-day listening + grammar (questions answerable from each article)
# ---------------------------------------------------------------------------

ENRICHMENT: dict[int, dict] = {
    1: {
        "listening": {
            "partFocus": "Part 1",
            "minutes": 40,
            "warmUp": "用網站 TTS 播放本日英文文章兩次：第一次只聽大意（地點、活動、招募重點），第二次邊聽邊記下職缺類型與申請文件。",
            "externalDrill": "今日外練 TOEIC Part 1：找 10 題照片描述題，先遮選項聽關鍵動作／人物／物件，再對答案；特別注意「正在做什麼」與背景細節。",
            "shadowTip": "跟讀第二、三段：放慢至 0.9 倍速，模仿 application form、resume、reference 等字串的重音與節奏。",
            "questions": [
                _q("Where was the job fair held?", ["At a university campus", "At Westbridge Convention Hall", "At a shopping mall", "At an airport lounge"], 1, "開場提到 At Westbridge Convention Hall。"),
                _q("What must applicants send before meeting a hiring team?", ["Only a resume", "An application form, a resume, and one reference", "A passport and bank statement", "Only a technical certificate"], 1, "文中要求 application form、resume 與 one reference。"),
                _q("Which roles did one company plan to hire?", ["Only accountants", "A secretary, a sales consultant, and engineering trainees", "Only part-time cashiers", "Only senior directors"], 1, "公司打算雇用秘書、業務顧問與工程受訓者。"),
                _q("What especially impressed the HR manager?", ["Applicants who avoided talking about goals", "Applicants who identified past achievements and linked them to long-term goals", "Applicants who refused training", "Applicants who only asked about wages"], 1, "人資重視能說明過往成就如何支持公司長期目標的人。"),
            ],
        },
        "grammar": {
            "focus": "詞性",
            "tip": "先判斷空格要填名詞、形容詞還是副詞；職涯文章常考 professional / professionally、eligible / eligibility。",
            "questions": [
                _q("Each applicant was asked to submit _____ resume before the interview.", ["they", "their", "them", "theirs"], 1, "空格後有名詞 resume，需所有格 their。"),
                _q("Candidates with strong communication _____ were more likely to be interviewed.", ["proficient", "proficiency", "proficiently", "profess"], 1, "strong 修飾名詞，故用 proficiency。"),
                _q("The company offered fair wages and _____ training for new hires.", ["structure", "structured", "structuring", "structures"], 1, "修飾 training 用過去分詞／形容詞 structured。"),
                _q("She felt slightly _____ before meeting the hiring team.", ["apprehension", "apprehensive", "apprehensively", "apprehend"], 1, "feel + 形容詞 → apprehensive。"),
                _q("Those with a college degree were more _____ for an interview.", ["eligible", "eligibility", "eligibly", "elope"], 0, "be + 形容詞 → eligible。"),
            ],
        },
    },
    2: {
        "listening": {
            "partFocus": "Part 2",
            "minutes": 40,
            "warmUp": "用 TTS 聽本日政策通知文章：先抓「誰發布、為何修訂、員工必須做什麼」，再複聽緊急事件與機密資訊相關句子。",
            "externalDrill": "今日外練 TOEIC Part 2：做 20 題應答題，練習 Wh- 問句與 Yes/No；遇到政策／規定類問句，先抓 must / should / report。",
            "shadowTip": "跟讀「must wear / must adhere / refrain from」等義務句，注意否定與禁止語氣的語調下降。",
            "questions": [
                _q("Who issued the revised office policy?", ["The marketing team", "The legal department", "The cafeteria staff", "The travel agency"], 1, "法務部門 recently issued a revised office policy。"),
                _q("What must staff display while on duty?", ["A parking ticket", "Identification", "A sales brochure", "A vacation form"], 1, "須穿著正式服裝並 display identification。"),
                _q("What should employees do in case of emergency or suspected theft?", ["Solve it alone", "Report the incident immediately", "Ignore the notice", "Leave supplies in open areas"], 1, "應立即回報，而非自行處理。"),
                _q("When is an exception to the new rules allowed?", ["Whenever employees feel busy", "Only with written approval from a senior manager", "If visitors ask politely", "During lunch only"], 1, "除非資深主管書面核准，否則沒有例外。"),
            ],
        },
        "grammar": {
            "focus": "主謂一致",
            "tip": "主詞是 each / every / the company 時動詞用單數；複數 staff members 才用複數動詞。",
            "questions": [
                _q("All staff members _____ wear proper business attire while on duty.", ["must", "musts", "is must", "are must"], 0, "情態動詞 must 後接原形，主詞複數不影響 must 形式。"),
                _q("The legal department _____ a revised office policy last week.", ["issue", "issues", "issued", "issuing"], 2, "過去時間 last week → 過去式 issued。"),
                _q("There _____ no exception unless written approval is given.", ["is", "are", "be", "were"], 0, "主詞 exception 為單數 → is。"),
                _q("Employees who enter restricted areas without permission _____ subject to review.", ["is", "are", "be", "was"], 1, "主詞 Employees（複數）→ are。"),
                _q("A recent inspection _____ that supplies were left in open areas.", ["show", "shows", "showed", "showing"], 2, "敘述已發生的檢查結果 → showed。"),
            ],
        },
    },
    3: {
        "listening": {
            "partFocus": "Part 1",
            "minutes": 40,
            "warmUp": "用 TTS 聽行政日常：注意 Mina 的任務、截止時間，以及工作坊教了哪些歸檔步驟。",
            "externalDrill": "今日外練 Part 1：選辦公室場景照片題 10 題，練習描述「坐在電腦前、修理印表機、整理文件」等動作。",
            "shadowTip": "跟讀 Mina 段落：注意 placed / fixed / prepared 過去式字尾 /t/ /d/ 的輕讀。",
            "questions": [
                _q("When does the administrative division begin its routine?", ["After lunch", "Before rush hour", "At midnight only", "On weekends only"], 1, "行政部門在尖峰時段前開始日常工作。"),
                _q("What was Mina asked to do?", ["Edit product information and submit it to the marketing manager", "Cancel the workshop", "Interview new staff", "Design a new logo"], 0, "Mina 需編輯產品資訊並提交給行銷經理。"),
                _q("Why did the supervisor hold a short workshop?", ["To raise salaries", "To acquaint new staff with internal filing methods", "To close the office", "To sell printers"], 1, "因為新進員工，要熟悉內部歸檔方法。"),
                _q("When was Mina's electronic file due?", ["Before the noon deadline", "After midnight", "Next month", "Only on Friday"], 0, "需在中午前以電子方式送出。"),
            ],
        },
        "grammar": {
            "focus": "介系詞",
            "tip": "submit to（提交給某人）、on the tabletop、before the deadline、under pressure 是行政情境高頻搭配。",
            "questions": [
                _q("Mina submitted the file _____ the marketing manager before noon.", ["to", "for", "at", "by"], 0, "submit A to B = 把 A 交給 B。"),
                _q("She placed her laptop _____ the tabletop.", ["on", "in", "at", "between"], 0, "放在桌面上用 on。"),
                _q("Employees learned how to store reports _____ the proper file system.", ["in", "on", "at", "with"], 0, "store … in a system/file。"),
                _q("Those who can concentrate _____ pressure may move into advanced positions.", ["under", "over", "above", "among"], 0, "under pressure 為固定搭配。"),
                _q("The supervisor held a workshop to acquaint everyone _____ filing methods.", ["with", "to", "for", "by"], 0, "acquaint A with B。"),
            ],
        },
    },
    4: {
        "listening": {
            "partFocus": "Part 2",
            "minutes": 40,
            "warmUp": "用 TTS 聽設備與責任文章：抓新進員工的任務清單、影印問題，以及接待客戶時的動作。",
            "externalDrill": "今日外練 Part 2：練習「Who / Where / What should I do?」類問句 20 題，對照辦公室指示與責任用語。",
            "shadowTip": "跟讀 accountable / confidential / skillfully，把重音放在倒數第二或第三音節上。",
            "questions": [
                _q("What did the new employee need to do before starting tasks?", ["Log on to the company server and check uploaded files", "Leave the office early", "Cancel the store opening", "Ignore the directory"], 0, "須先登入伺服器並確認最新檔案。"),
                _q("Why did he make a duplicate page?", ["Because one page was missing", "Because the client refused", "Because the server crashed permanently", "Because the bookshelf was full"], 0, "少了一頁所以影印複本。"),
                _q("Where were the materials later arranged?", ["On a bookshelf next to the reception desk", "In the parking lot", "In the cafeteria kitchen", "On the roof"], 0, "資料後來放在接待櫃台旁書架。"),
                _q("What did the employee check when a client arrived?", ["Her visitor code on the keypad", "Her vacation schedule", "Her salary records", "Her shopping list"], 0, "用鍵盤確認訪客代碼。"),
            ],
        },
        "grammar": {
            "focus": "連接詞",
            "tip": "because / especially when / and / before 用來連接原因、時間與並列責任，避免只用逗號硬接。",
            "questions": [
                _q("He made a duplicate _____ one page was missing.", ["because", "although", "unless", "despite"], 0, "表示原因用 because。"),
                _q("Employees should never procrastinate, _____ when handling confidential information.", ["especially", "despite", "unless", "neither"], 0, "especially when = 尤其當……時。"),
                _q("_____ starting the task, he logged on to the server.", ["Before", "During", "While", "Afterward"], 0, "在開始任務之前 → Before。"),
                _q("He greeted the client _____ checked her visitor code.", ["and", "but", "or", "nor"], 0, "兩個連續動作用 and 連接。"),
                _q("Every small assignment contributes to the larger operation, _____ it seems simple.", ["even if", "so that", "in case", "as if"], 0, "even if = 即使看起來簡單。"),
            ],
        },
    },
    5: {
        "listening": {
            "partFocus": "Part 1",
            "minutes": 40,
            "warmUp": "用 TTS 聽商務溝通文章：先抓旅行者攜帶物品與報告截止，再聽文件備份與會議溝通重點。",
            "externalDrill": "今日外練 Part 1：挑「手提箱、櫃台、檔案櫃、列印」相關照片題，練習物件與人物位置描述。",
            "shadowTip": "跟讀 compile / promptly / permanently，對齊母音長度，避免把 -ly 副詞唸得過重。",
            "questions": [
                _q("What did the business traveler bring?", ["A briefcase, a timetable, and several folders", "Only a camera", "Sports equipment", "Kitchen tools"], 0, "攜帶公事包、時間表與多個資料夾。"),
                _q("Why did the staff compile data promptly?", ["Because the report was due soon", "Because the office closed forever", "Because printing was banned", "Because no meeting was planned"], 0, "報告即將到期。"),
                _q("What must be done before the next forum?", ["The material must be revised", "The company must fire the team", "All emails must be deleted", "The briefcase must be sold"], 0, "經理要求下次論壇前修訂資料。"),
                _q("Why was a replacement set of documents prepared?", ["In case anything was concealed or misplaced", "To decorate the lobby", "For a music concert", "For tax-free shopping"], 0, "預防文件被藏匿或放錯。"),
            ],
        },
        "grammar": {
            "focus": "時態",
            "tip": "敘述已抵達／已檢查用過去式；公司計畫與規定可用過去 said + would/must 表轉述。",
            "questions": [
                _q("A business traveler _____ at the office with a briefcase yesterday.", ["arrive", "arrived", "arrives", "arriving"], 1, "yesterday 線索 → 過去式 arrived。"),
                _q("The manager said the material _____ be revised before the next forum.", ["must", "musts", "musting", "to must"], 0, "轉述義務仍用 must + 原形。"),
                _q("While one assistant _____ the printing, another organized the cabinet.", ["handled", "handle", "handles", "handling"], 0, "過去進行中的分工，文中用過去式並列 handled。"),
                _q("The company planned to implement a new system _____.", ["permanently", "permanent", "permanence", "permanency"], 0, "修飾動詞 implement 用副詞 permanently。"),
                _q("By the meeting time, the team _____ the data promptly.", ["had compiled", "compile", "compiles", "compiling"], 0, "強調會議前已完成可用過去完成 had compiled。"),
            ],
        },
    },
    6: {
        "listening": {
            "partFocus": "Part 2",
            "minutes": 40,
            "warmUp": "用 TTS 聽藝文活動：記下展覽地點、名人作者行程、門票含什麼，以及義賣收益用途。",
            "externalDrill": "今日外練 Part 2：練習活動邀請與時間地點問答（When / Where / Who will…），各做 15 題。",
            "shadowTip": "跟讀 exhibition / manuscript / donation，注意 /ʃ/ 與重音落在第二音節。",
            "questions": [
                _q("What did the local gallery announce?", ["A weekend exhibition", "A factory shutdown", "A bank merger", "A flight delay"], 0, "藝廊宣布週末展覽。"),
                _q("Where did the celebrity author give a short presentation?", ["In the theater", "At the airport", "In a factory", "On a highway"], 0, "下午在劇場做簡短演講。"),
                _q("What would book-sale proceeds support?", ["A donation program for the public library", "A private yacht", "A parking fine", "A chemical plant"], 0, "收益支持公共圖書館捐贈計畫。"),
                _q("What did each banquet ticket include?", ["A small collection of antique items on display", "A free car", "Unlimited flights", "A hospital checkup"], 0, "門票含展示的小型古董收藏。"),
            ],
        },
        "grammar": {
            "focus": "詞性／主謂一致",
            "tip": "admission / admission was required；many alumni planned（複數）；the show was carefully planned（被動語意＋形容詞）。",
            "questions": [
                _q("Many alumni from the museum _____ to attend with their families.", ["plan", "plans", "planned", "planning"], 2, "敘述過去計畫 → planned；alumni 複數但不影響過去式形態。"),
                _q("The organizer said that _____ was required for the banquet.", ["admit", "admission", "admissive", "admittedly"], 1, "主詞位置需要名詞 admission。"),
                _q("Proceeds from the sale would support a _____ program.", ["donate", "donation", "donated", "donating"], 1, "名詞 donation program。"),
                _q("The event was designed to be informative and _____ to the community.", ["benefit", "beneficial", "beneficially", "benefited"], 1, "be + 形容詞 beneficial。"),
                _q("The current issue of the journal _____ available nearby.", ["was", "were", "are", "be"], 0, "issue 單數 → was。"),
            ],
        },
    },
    7: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 完整聽市場調查文章兩遍：第一遍抓調查結論，第二遍記下策略（promotion、comparison charts、stores）。本日為聽力綜合日。",
            "externalDrill": "今日 LC Mixed：Part 1 五題＋Part 2 十題，限時 25 分鐘；錯題只複習「訊號詞」不盯原文翻譯。",
            "shadowTip": "跟讀 competitively / aggressively / positively 等 -ly 副詞，保持句尾語調自然落下。",
            "questions": [
                _q("What did the public relations department conduct?", ["A survey on seasonal campaigns", "A cooking class", "A medical exam", "A flight training"], 0, "公關部進行季節性活動調查。"),
                _q("What did many buyers prefer?", ["Clear demonstrations rather than informal advertising", "No product information", "Only handwritten ads", "Silent stores"], 0, "買家偏好清楚示範而非非正式廣告。"),
                _q("What would the brand reserve resources for?", ["Online comparison charts", "Closing all stores", "Deleting surveys", "Canceling promotions"], 0, "額外資源留給線上比較表。"),
                _q("What did the analyst say about the performance gap?", ["It had narrowed", "It had disappeared forever", "It had doubled overnight", "It was never measured"], 0, "現況與理想目標的差距已縮小。"),
            ],
        },
        "grammar": {
            "focus": "介系詞／時態",
            "tip": "respond to campaigns；based on analysis；is expected to rise — 調查報告常用現在完成／被動預期。",
            "questions": [
                _q("The survey analyzed how customers respond _____ seasonal campaigns.", ["to", "for", "at", "with"], 0, "respond to = 對……做出反應。"),
                _q("_____ the analysis, the company expanded its marketplace strategy.", ["Based on", "Based in", "Based at", "Based for"], 0, "Based on = 根據。"),
                _q("Demand for the product is expected _____ continue rising.", ["to", "for", "at", "in"], 0, "be expected to + V。"),
                _q("The plan was not postponed _____ management believed it would help sales.", ["because", "despite", "unless", "although"], 0, "原因用 because。"),
                _q("The impact of the new strategy _____ already visible in several stores.", ["was", "were", "are", "be"], 0, "impact 單數 → was。"),
            ],
        },
    },
    8: {
        "listening": {
            "partFocus": "Part 3",
            "minutes": 40,
            "warmUp": "用 TTS 把文章當 Part 3 對話素材：聽書店活動目的、行銷策略與品牌形象提醒。",
            "externalDrill": "今日外練 Part 3：做 3 組對話（9 題），先看題幹再聽；練習抓 Who / Why / What will happen next。",
            "shadowTip": "跟讀 brand image / consumer preferences / incentive，模擬對話中第二人附和的語調。",
            "questions": [
                _q("Where was the best-selling author invited to meet consumers?", ["At a downtown shop", "At a hospital", "At a factory gate", "At a police station"], 0, "在市中心書店與消費者見面。"),
                _q("What did staff observe in the small experiment?", ["How customers reacted to displays, samples, and a sales target", "How to close the shop forever", "How to cancel subscriptions", "How to fire photographers"], 0, "觀察顧客對陳列、樣品與銷售目標的反應。"),
                _q("What must the company not disregard?", ["The importance of brand image", "The need to delete ads", "Parking tickets", "Weather forecasts only"], 0, "分析師提醒不可忽視品牌形象。"),
                _q("According to the team, what produces the best results?", ["Steady effort, clear goals, and a strong incentive", "Ignoring customers", "Removing all displays", "Stopping early subscriptions"], 0, "文末強調持續努力、清楚目標與誘因。"),
            ],
        },
        "grammar": {
            "focus": "被動語態",
            "tip": "活動與廣告常用 be launched / be invited / be made；主詞是活動或訊息時優先想被動。",
            "questions": [
                _q("A celebration campaign _____ by the bookstore last weekend.", ["was launched", "launched", "was launching", "has launch"], 0, "campaign 是被推出 → was launched。"),
                _q("A best-selling author _____ to meet consumers downtown.", ["was invited", "invited", "was inviting", "invite"], 0, "作者被邀請 → was invited。"),
                _q("Every effort should _____ to resolve customer doubts.", ["be made", "make", "made", "making"], 0, "effort should be made。"),
                _q("If preferences _____ accurately, the campaign will have more impact.", ["are detected", "detect", "are detecting", "detected"], 0, "preferences 被偵測 → are detected。"),
                _q("The display was obviously _____ to many visitors.", ["appealing", "appealed", "appeal", "appeals"], 0, "be + 形容詞 appealing。"),
            ],
        },
    },
    9: {
        "listening": {
            "partFocus": "Part 4",
            "minutes": 40,
            "warmUp": "用 TTS 把文章當 Part 4 簡報：聽 CEO 宣布、分析師數據，以及合併與風險警告。",
            "externalDrill": "今日外練 Part 4：做 3 篇短講（9 題），練習財經簡報中的 trend / merge / warning 關鍵句。",
            "shadowTip": "跟讀 optimistic / substantial / stagnant，用演講腔把重點字略微拉長。",
            "questions": [
                _q("Why would business hours be adjusted?", ["To speed up trading and improve service", "To close the factory permanently", "To cancel all reports", "To stop hiring"], 0, "為了加速交易並改善服務。"),
                _q("What did the analyst say about the industry?", ["It was still healthy despite unstable months", "It had completely collapsed", "It banned all mergers", "It stopped reviewing figures"], 0, "產業仍健康，儘管有不穩月份。"),
                _q("What did the company decide to do?", ["Merge with a private partner", "Remain alone forever", "Sell only to competitors", "Ignore all indicators"], 0, "決定與私人夥伴合併。"),
                _q("What risk did the director warn about?", ["Prosperity could wane if long-term consequences were ignored", "Prices would never change", "Boom was guaranteed forever", "Reports were unnecessary"], 0, "若忽略長期後果，繁榮可能衰退。"),
            ],
        },
        "grammar": {
            "focus": "不定詞／動名詞",
            "tip": "decide to merge；aimed at improving；keep a close eye on — 記住 to V 與 V-ing 搭配差異。",
            "questions": [
                _q("The company decided _____ with a private partner.", ["to merge", "merging", "merge", "merged"], 0, "decide to + V。"),
                _q("Management believed the contribution to future growth would be _____.", ["substantial", "substantially", "substance", "substantiate"], 0, "be + 形容詞 substantial。"),
                _q("The director warned that prosperity could wane if the team ignored _____ consequences.", ["long-term", "long-termed", "longer", "longest"], 0, "複合形容詞 long-term 修飾 consequences。"),
                _q("The firm promised _____ productivity over the coming period.", ["to boost", "boosting", "boost", "boosted"], 0, "promise to + V。"),
                _q("Some branches remained limited by _____ operations.", ["costly", "cost", "costs", "costing"], 0, "形容詞 costly 修飾 operations。"),
            ],
        },
    },
    10: {
        "listening": {
            "partFocus": "Part 3",
            "minutes": 40,
            "warmUp": "用 TTS 聽零售情境：商品種類、免稅促銷、分期與保固說明。把內容想像成店員與顧客對話。",
            "externalDrill": "今日外練 Part 3：選購物／退換貨對話 3 組，練習 price / warranty / installment 聽取。",
            "shadowTip": "跟讀 installments / redeemable / authentic，注意多音節字的次重音。",
            "questions": [
                _q("What was the store offering for a limited time?", ["A tax-free promotion", "Free houses", "Unlimited flights", "Medical surgery"], 0, "限時免稅促銷。"),
                _q("What did the sales assistant explain carefully?", ["Price, warranty, and receipt process", "Only the weather", "Only flight times", "Only office policy"], 0, "說明價格、保固與收據流程。"),
                _q("Why did the customer purchase in installments?", ["Because the charge was more acceptable that way", "Because cash was required only", "Because the store refused cards", "Because items were free"], 0, "分期讓費用較可接受。"),
                _q("What else did regular subscribers receive?", ["Clearance discounts and redeemable benefits", "A factory tour only", "A passport", "A merger contract"], 0, "還有清倉折扣與可兌換福利。"),
            ],
        },
        "grammar": {
            "focus": "關係代名詞",
            "tip": "that / which 修飾商品或促銷；who 修飾顧客。先找先行詞再選關係詞。",
            "questions": [
                _q("She looked for a necklace _____ would fit her new costume.", ["that", "who", "whose", "where"], 0, "先行詞 necklace（物）→ that/which。"),
                _q("The cashier reminded customers _____ items were marked clearly.", ["that", "what", "which", "whom"], 0, "remind + that 子句。"),
                _q("The vendor could provide a product _____ on the shopper's preference.", ["depending", "depend", "depends", "dependent"], 0, "depending on = 取決於。"),
                _q("Another shopper _____ was checking labels made a careful choice.", ["who", "which", "where", "what"], 0, "修飾人 shopper → who。"),
                _q("The store kept shelves tidy for every visitor _____ came before closing.", ["who", "which", "what", "where"], 0, "visitor 是人 → who。"),
            ],
        },
    },
    11: {
        "listening": {
            "partFocus": "Part 4",
            "minutes": 40,
            "warmUp": "用 TTS 聽產品發表會：新裝置特點、專利、市場與投資人興趣，當成 Part 4 技術簡報。",
            "externalDrill": "今日外練 Part 4：選產品發表／研發報告 3 篇，練習 feature / patent / distribution 關鍵資訊。",
            "shadowTip": "跟讀 revolutionary / innovative / compatible，把科技詞拆音節慢練再加速。",
            "questions": [
                _q("What was the new device designed to improve?", ["The quality of home appliances", "Airport security only", "Restaurant menus", "Bank interest rates"], 0, "改善家電品質。"),
                _q("Where was the invention handmade and tested?", ["In the laboratory", "In a bakery", "On a beach", "In a theater"], 0, "在實驗室手工製作並反覆測試。"),
                _q("What did the new product feature?", ["A revolutionary sensor and an innovative control system", "Only a wooden crate", "A banquet ticket", "A customs form"], 0, "革命性感測器與創新控制系統。"),
                _q("What did several investors express by the end?", ["Interest in the project", "Anger about lunch", "Plans to ban patents", "Refusal to meet again"], 0, "多位投資人表示興趣。"),
            ],
        },
        "grammar": {
            "focus": "條件句",
            "tip": "If feedback is positive, we will upgrade…；科技文常用 If + 現在，will + 原形表真實條件。",
            "questions": [
                _q("If the device _____ repeatedly, breakdowns can be avoided.", ["is tested", "tested", "testing", "tests"], 0, "真實條件被動：is tested。"),
                _q("The team will extend the patent if funding _____.", ["increases", "increase", "increased", "increasing"], 0, "if + 現在簡單式。"),
                _q("The product will be available for distribution once testing _____ successful.", ["is", "are", "be", "were"], 0, "testing 當不可數／單數概念 → is。"),
                _q("Customers will buy more units if the design _____ reliable.", ["remains", "remain", "remaining", "remained"], 0, "if 子句第三人稱單數 remains。"),
                _q("If investors _____ interest, a follow-up meeting will be held.", ["express", "expresses", "expressing", "expressed"], 0, "複數 investors → express。"),
            ],
        },
    },
    12: {
        "listening": {
            "partFocus": "Part 3",
            "minutes": 40,
            "warmUp": "用 TTS 聽工廠改建：自動化原因、安全規範、化學外洩與產能目標，想像成廠長與工程師對話。",
            "externalDrill": "今日外練 Part 3：工廠／維修對話 3 組，抓 shortage / safety / productivity。",
            "shadowTip": "跟讀 automate / specifications / economize，注意美式重音位置。",
            "questions": [
                _q("Why did the manufacturer plan to renovate and automate?", ["Because of a shortage of raw materials and the need for efficiency", "To open a restaurant", "To cancel all orders", "To stop safety training"], 0, "原料短缺與效率需求。"),
                _q("What were workers trained to do?", ["Operate devices, assemble parts, and fill orders quickly", "Ignore specifications", "Close the plant permanently", "Delete inventory only"], 0, "操作設備、組裝零件並快速完成訂單。"),
                _q("What problem did the supervisor note during inspection?", ["The plant had been damaged by a chemical leak", "The plant had too many tourists", "All tools were brand new", "No schedule existed"], 0, "化學外洩造成損害。"),
                _q("What did the company aim to economize on?", ["Power, while also reducing waste", "Only employee names", "Banquet tickets", "Flight routes"], 0, "節省電力並減少浪費。"),
            ],
        },
        "grammar": {
            "focus": "Part 6 文意",
            "tip": "工廠文常見因果與目的：attributed to、in order to、so that；選詞時先看前後句邏輯。",
            "questions": [
                _q("The decision was attributed _____ a shortage of raw materials.", ["to", "for", "with", "by"], 0, "be attributed to = 歸因於。"),
                _q("Workers were trained to operate the devices _____.", ["properly", "proper", "property", "propose"], 0, "修飾動詞用副詞 properly。"),
                _q("Safety precautions were essential _____ every process could follow specifications.", ["so that", "despite", "because of", "unless"], 0, "so that = 以便／使……能夠。"),
                _q("The modification would _____ productivity across the lines.", ["increase", "increasing", "increased", "increases"], 0, "would + 原形 increase。"),
                _q("The director believed success _____ on careful planning.", ["depended", "depend", "depending", "depends"], 0, "過去敘述 depended on。"),
            ],
        },
    },
    13: {
        "listening": {
            "partFocus": "Part 4",
            "minutes": 40,
            "warmUp": "用 TTS 聽客服處理流程：抱怨內容、更換／退款承諾、主管對禮貌與透明度的要求。",
            "externalDrill": "今日外練 Part 4：客服廣播或訓練短講 3 篇，練習 complaint / replace / guarantee。",
            "shadowTip": "跟讀 courteously / inconvenience / satisfaction，把客服禮貌語調練得穩、清楚。",
            "questions": [
                _q("What were the complaints about?", ["A defective product that was incomplete with a damaged logo", "A missing passport", "A delayed merger", "A hotel banquet"], 0, "產品有瑕疵、不完整且標誌受損。"),
                _q("How did the agent respond?", ["Courteously, promising to handle the deal appropriately", "By ending the call immediately", "By refusing any help", "By raising the price"], 0, "有禮貌並承諾妥善處理。"),
                _q("What could the company do if necessary?", ["Replace the product and return the payment", "Ban the customer", "Delete the logo only", "Ignore the evaluation"], 0, "必要時更換並退款。"),
                _q("What did the supervisor say satisfaction depended on?", ["Clear communication", "Longer hold music", "Higher prices only", "Fewer notifications"], 0, "滿意度取決於清楚溝通。"),
            ],
        },
        "grammar": {
            "focus": "被動／不定詞",
            "tip": "complaints were received；promised to handle；invited to visit — 客服用被動＋不定詞很頻繁。",
            "questions": [
                _q("A couple of complaints _____ about a defective product.", ["were received", "received", "was received", "receiving"], 0, "complaints 複數被收到 → were received。"),
                _q("The agent promised _____ the issue appropriately.", ["to handle", "handling", "handle", "handled"], 0, "promise to + V。"),
                _q("The customer was invited _____ the site to confirm details.", ["to visit", "visiting", "visit", "visited"], 0, "be invited to + V。"),
                _q("The evaluation of the complaint would be completed _____.", ["promptly", "prompt", "promptness", "prompts"], 0, "修飾 completed 用副詞 promptly。"),
                _q("Several cases had been _____ successfully by the end of the shift.", ["solved", "solve", "solving", "solves"], 0, "過去完成被動 had been solved。"),
            ],
        },
    },
    14: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 完整聽旅遊航空文章兩遍：海關、商務艙、行李遺失與後續旅遊。本日為聽力綜合複習日。",
            "externalDrill": "今日 LC Mixed：Part 2 十題＋Part 3 一組＋Part 4 一篇，計時完成；錯題標註是「細節」還是「主旨」失誤。",
            "shadowTip": "跟讀 itinerary / declare / proximity，模擬機場廣播速度再降回跟讀速度。",
            "questions": [
                _q("What did the agent remind the traveler to do?", ["Fill out the customs form and declare dutiable items", "Skip passport control", "Leave the suitcase unattended", "Cancel the itinerary"], 0, "填寫海關表並申報應稅物品。"),
                _q("Which class did the passenger board?", ["Business class", "Only cargo class", "No seat assigned", "Train first class only"], 0, "搭乘商務艙。"),
                _q("What problem occurred upon arrival?", ["His baggage was missing", "His passport was fake", "The beach was closed forever", "The hotel refused tourists"], 0, "抵達後發現行李遺失。"),
                _q("Where did staff promise to ship the luggage?", ["To his hotel", "To the factory", "To a bookstore", "To a bank branch"], 0, "答應盡快送到飯店。"),
            ],
        },
        "grammar": {
            "focus": "關係子句／條件句",
            "tip": "items that might be subject to duty；if baggage is missing, contact the carrier — 旅遊文常混用關係子句與條件。",
            "questions": [
                _q("Declare any items _____ might be subject to duty.", ["that", "who", "whom", "whose"], 0, "修飾 items → that。"),
                _q("If baggage _____ missing, contact the carrier promptly.", ["is", "are", "be", "were"], 0, "baggage 不可數 → is。"),
                _q("The staff promised _____ the luggage to the hotel.", ["to ship", "shipping", "ship", "shipped"], 0, "promise to + V。"),
                _q("He enjoyed a journey _____ was comfortable and superb.", ["that", "who", "where", "what"], 0, "修飾 journey → that。"),
                _q("The proximity to attractions made the trip _____ enjoyable.", ["even more", "even most", "more even", "most even"], 0, "even more + 形容詞。"),
            ],
        },
    },
    15: {
        "listening": {
            "partFocus": "Part 3",
            "minutes": 40,
            "warmUp": "用 TTS 聽合約談判：條款、反對、修訂報價、締約期限與最終和解，當成雙方會議對話。",
            "externalDrill": "今日外練 Part 3：商務會議對話 3 組，重點聽 objection / revise / deadline / settlement。",
            "shadowTip": "跟讀 stipulation / terminate / settlement，把法律商務詞唸清楚再加快。",
            "questions": [
                _q("What did the proposal include regarding confidentiality?", ["A clear stipulation", "No terms at all", "Only a joke clause", "A travel itinerary"], 0, "提案含明確的保密條款。"),
                _q("What did one side threaten if conflict continued?", ["To terminate the agreement", "To increase hospitality only", "To donate books", "To renovate a factory"], 0, "威脅終止協議。"),
                _q("What was required before the deadline?", ["A signature", "A picnic basket", "A sensor patent", "A boarding pass"], 0, "期限前需要簽名。"),
                _q("What did the teams finally reach?", ["A settlement and agreement to renew the contract", "A decision to never meet", "A plan to ignore trust", "A ban on alliances"], 0, "達成和解並同意續約。"),
            ],
        },
        "grammar": {
            "focus": "進階詞彙題",
            "tip": "negotiate / settlement / stipulation / terminate 常作 Part 5 詞彙題；先看句子要「協議結果」還是「終止動作」。",
            "questions": [
                _q("The two firms entered into a _____ to finalize the alliance.", ["negotiation", "negotiate", "negotiable", "negotiator"], 0, "entered into a negotiation。"),
                _q("One side threatened to _____ the agreement if talks failed.", ["terminate", "termination", "terminal", "term"], 0, "threatened to + V → terminate。"),
                _q("A clear _____ regarding confidentiality was included.", ["stipulation", "stipulate", "stipulated", "stipulating"], 0, "需要名詞 stipulation。"),
                _q("After hours of discussion, both parties reached a _____.", ["settlement", "settle", "settled", "settling"], 0, "reach a settlement。"),
                _q("They agreed to _____ the scope of the project.", ["narrow", "narrowly", "narrowness", "narrowed"], 0, "agree to + V → narrow。"),
            ],
        },
    },
    16: {
        "listening": {
            "partFocus": "Part 4",
            "minutes": 40,
            "warmUp": "用 TTS 聽出版供應鏈簡報：庫存確認、批量折扣、通路配送與寄售協議。",
            "externalDrill": "今日外練 Part 4：物流／訂單短講 3 篇，練習 inventory / invoice / consignment。",
            "shadowTip": "跟讀 distribution / consignment / affordability，維持簡報節奏的停頓。",
            "questions": [
                _q("What did the client ask the supplier to confirm before finalizing the order?", ["The inventory, via a detailed checklist", "The weather only", "Employee vacations", "Flight entertainment"], 0, "要求詳細清單並確認庫存。"),
                _q("When would the invoice be sent?", ["Shortly", "Never", "After ten years", "Only after the store closed"], 0, "發票即將寄出。"),
                _q("What discount did the dealer offer?", ["A discount on bulk purchases", "Free houses", "Unlimited surgery", "Tax-free flights only"], 0, "大批量採購折扣。"),
                _q("What agreement would be finalized soon?", ["The consignment agreement", "A sports contract", "A medical leave form", "A picnic permit"], 0, "寄售協議即將敲定。"),
            ],
        },
        "grammar": {
            "focus": "易混淆字",
            "tip": "affect/effect、price/prize、assure/ensure、stock/stake — 供應鏈題常考形近義近字。",
            "questions": [
                _q("The new trend would _____ the distribution of books.", ["affect", "effect", "affection", "effective"], 0, "動詞「影響」用 affect。"),
                _q("The manager said each selection's cost must be measured _____.", ["carefully", "careful", "care", "caring"], 0, "副詞 carefully。"),
                _q("The dealer offered a discount on _____ purchases.", ["bulk", "bulky", "bulletin", "bulb"], 0, "bulk purchases = 大宗採購。"),
                _q("They will _____ the clientele of satisfactory service.", ["assure", "ensure", "insure", "secure"], 0, "assure someone of…；ensure 後直接接事。此處有 clientele → assure。"),
                _q("The commodity was _____ at a competitive price.", ["quoted", "quieted", "quilted", "quitted"], 0, "quoted = 報價。"),
            ],
        },
    },
    17: {
        "listening": {
            "partFocus": "Part 3",
            "minutes": 40,
            "warmUp": "用 TTS 聽物流運送：包裝、冷藏、重量檢查、易碎易腐與簽收，想像調度員與司機對話。",
            "externalDrill": "今日外練 Part 3：運送／取件對話 3 組，抓 crate / perishable / signature / due date。",
            "shadowTip": "跟讀 perishable / adequately / correspondence，注意咬字清晰避免吞音。",
            "questions": [
                _q("How were the goods packed and stored?", ["In a wooden crate in a cold facility", "In open sunlight only", "In a theater seat", "In a picnic basket"], 0, "木箱包裝並置於冷藏設施。"),
                _q("What did the driver check before departure?", ["The weight, after getting a ticket for the load", "Only the museum gift shop", "Only banquet recipes", "Only stock prices"], 0, "取得載運單據並檢查重量。"),
                _q("Why did the courier handle the shipment carefully?", ["Because some items were fragile and perishable", "Because items were digital only", "Because no due date existed", "Because the van was empty forever"], 0, "部分貨物易碎且易腐。"),
                _q("What did the agency ask the recipient to do?", ["Affix a signature", "Delete the notice", "Refuse all packages", "Open every crate outdoors"], 0, "要求收件人簽名。"),
            ],
        },
        "grammar": {
            "focus": "正式商務語氣",
            "tip": "正式物流用語偏好 ensure / request that / prior to；少用口語 get / stuff。",
            "questions": [
                _q("The courier _____ that the shipment was handled adequately.", ["ensured", "ensure", "ensuring", "ensures"], 0, "過去敘述 ensured。"),
                _q("Please complete the shipping process _____ the due date.", ["before", "ago", "since", "during"], 0, "在到期日之前 → before。"),
                _q("The recipient was asked to _____ a signature on the notice.", ["affix", "fix", "affect", "effect"], 0, "affix a signature 為正式用法。"),
                _q("Every step must be handled correctly to avoid _____ delivery.", ["incorrect", "correct", "correctly", "correcting"], 0, "形容詞 incorrect 修飾 delivery。"),
                _q("The goods were stored carefully _____ temperature control.", ["for", "to", "at", "by"], 0, "for = 為了溫度控制。"),
            ],
        },
    },
    18: {
        "listening": {
            "partFocus": "Part 4",
            "minutes": 40,
            "warmUp": "用 TTS 聽餐飲服務短講：自助餐、廚師備料、招待與預約流程。",
            "externalDrill": "今日外練 Part 4：餐廳／宴會廣播 3 篇，練習 buffet / complimentary / reservation。",
            "shadowTip": "跟讀 complimentary / refreshments / amenities，維持服務業禮貌語氣。",
            "questions": [
                _q("Where was the delicious dessert served?", ["In the dining room", "In the garage", "On the highway", "In the laboratory"], 0, "甜點在餐廳供應。"),
                _q("What did the chef add while preparing the seafood meal?", ["Garlic, with a spicy sauce", "Only wooden crates", "Only patents", "Only customs forms"], 0, "加入蒜頭並搭配辣醬。"),
                _q("What might guests receive after checking in?", ["A complimentary dish prepared by the chef", "A factory sensor", "A merger contract", "A delinquent notice"], 0, "報到後可能獲得主廚招待菜。"),
                _q("What did the team arrange in advance?", ["Refreshments and a caterer reservation", "A chemical leak inspection", "A stock market IPO only", "A subway detour"], 0, "事先安排茶點與外燴預約。"),
            ],
        },
        "grammar": {
            "focus": "長句結構",
            "tip": "先抓主要動詞，再看 while / before / including 引導的附加資訊，避免被插入語帶跑。",
            "questions": [
                _q("_____ using the dishwasher, the chef prepared a seafood meal.", ["After", "During", "Between", "Among"], 0, "After + V-ing。"),
                _q("Guests were asked to check in before staff _____ a complimentary dish.", ["would compensate with", "compensate", "compensating", "compensates"], 0, "文意為報到後才提供招待；原句結構用 would compensate with。"),
                _q("The cook tasted the dish _____ serving it.", ["before", "ago", "since", "for"], 0, "before serving。"),
                _q("Every amenity, _____ care for belongings, was designed to ease discomfort.", ["including", "include", "includes", "included"], 0, "插入語用 including。"),
                _q("The cuisine followed a set sequence, _____ an extensive menu.", ["offering", "offer", "offered", "offers"], 0, "分詞構句 offering。"),
            ],
        },
    },
    19: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 聽財務營收段落兩遍：抓住 revenue projection、overseas vs domestic，忽略文中較雜訊的句子，訓練抓數字趨勢。",
            "externalDrill": "今日弱項 Mixed：Part 3 一組＋Part 4 一篇財報短講；專門練習 increase / decline / offset / projection。",
            "shadowTip": "跟讀 substantial / anticipated / projection，用平穩語氣讀數字相關句。",
            "questions": [
                _q("What did the revenue projection show?", ["A substantial increase, though some figures declined", "Only zero sales forever", "A ban on exports", "No change in fees"], 0, "營收預測大幅增加，但部分數字下降。"),
                _q("What could a fee-structure shift affect?", ["Production sales", "Only cafeteria recipes", "Only theater tickets", "Only weather"], 0, "可能影響生產銷售。"),
                _q("What offset the decline in overseas orders?", ["A domestic increase in revenue", "A permanent factory closure", "A canceled projection", "A lost passport"], 0, "國內營收增加抵銷海外訂單下降。"),
                _q("What will management do before revising the annual projection?", ["Anticipate further shift in demand", "Delete all figures", "Stop reviewing costs", "Ignore exports"], 0, "先預期需求再變動再修年預測。"),
            ],
        },
        "grammar": {
            "focus": "進階詞彙／易混淆字",
            "tip": "revenue / profit / projection / offset / decline — 先分清「營收」與「利潤」，再看升降動詞。",
            "questions": [
                _q("The revenue projection showed a substantial _____.", ["increase", "increasingly", "increased", "increases"], 0, "a substantial increase（名詞）。"),
                _q("Some figures _____ markedly last quarter.", ["declined", "decline", "declining", "declines"], 0, "過去式 declined。"),
                _q("The decline overseas was _____ by stronger domestic sales.", ["offset", "onset", "upset", "reset"], 0, "offset = 抵銷。"),
                _q("Management will revise the annual _____.", ["projection", "projectile", "projecting", "projector"], 0, "projection = 預測。"),
                _q("Rising profit slightly _____ higher costs.", ["offset", "offended", "offered", "opened"], 0, "利潤抵銷成本 → offset。"),
            ],
        },
    },
    20: {
        "listening": {
            "partFocus": "Part 3",
            "minutes": 40,
            "warmUp": "用 TTS 聽預算控管：委員會、刪減、審計減少赤字、季度計畫核可。想像財務會議對話。",
            "externalDrill": "今日外練 Part 3：預算會議對話 3 組，聽 budget cuts / audit / allocate / fiscal year。",
            "shadowTip": "跟讀 curtail / reimburse / inflation，把會議用語唸得乾脆。",
            "questions": [
                _q("What did a senior manager call some spending cuts?", ["Temporary, tied to the annual budget theme", "Permanent forever with no review", "Unrelated to policy", "Only about vacations"], 0, "部分刪減是暫時且與年度預算主題相關。"),
                _q("What did the audit confirm?", ["The financial deficit was substantially reduced", "All funds had disappeared", "Inflation had stopped forever", "No meetings were held"], 0, "審計確認赤字大幅減少。"),
                _q("When will staff allocate funds?", ["Once the inspector approves the preferred quarter plan", "Before any review", "Without reimbursement rules", "Only after the company closes"], 0, "稽核員核准季度計畫後。"),
                _q("What pushed departments to review fiscal planning more often?", ["Inflation", "A music festival", "A picnic", "A film premiere"], 0, "通膨促使更常檢視財政規劃。"),
            ],
        },
        "grammar": {
            "focus": "正式語氣／長句",
            "tip": "正式預算句常用 subject + will + V once…；避免口語 gonna / a lot of 取代 allocate / substantial。",
            "questions": [
                _q("Staff will allocate funds once the inspector _____ the plan.", ["approves", "approve", "approving", "approved"], 0, "once + 現在式（時間條件）。"),
                _q("The deficit was _____ reduced after the audit.", ["substantially", "substantial", "substance", "substantiate"], 0, "副詞 substantially。"),
                _q("The committee met frequently _____ review the team's capability.", ["to", "for", "at", "by"], 0, "met … to + V 表目的。"),
                _q("Cuts were tied _____ traditional policy.", ["to", "for", "at", "with"], 0, "be tied to。"),
                _q("Turnover figures were reviewed _____ the finance team.", ["by", "to", "for", "at"], 0, "被動語態 by + 行為者。"),
            ],
        },
    },
    21: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 聽併購文章兩遍：抓 partnership、relocate、select a partner to merge、protect assets；跳過雜訊句，練主旨聽力。本日 LC Mixed。",
            "externalDrill": "今日 LC Mixed 模考節奏：Part 1–4 各短練習一輪（約 40 分鐘），錯題只記「併購／擴張」類關鍵詞。",
            "shadowTip": "跟讀 relocate / foresee / simultaneously，用穩速讀完長句再加速。",
            "questions": [
                _q("When will management announce the plan?", ["Once interested, active parties accept it", "Only after bankruptcy", "Never", "Before any partnership talk"], 0, "有興趣且積極的各方接受後才宣布。"),
                _q("What does the firm plan regarding a strong competitor?", ["To relocate away while protecting its asset", "To ignore all assets", "To delete sales data", "To ban employee contributions"], 0, "計畫搬離強大競爭對手並保護資產。"),
                _q("What must employees be careful not to do?", ["Misplace considerable files", "Contribute in a dedicated way", "Grow sales", "Protect assets"], 0, "小心不要放錯重要檔案。"),
                _q("What will they select by year-end?", ["A partner to merge with", "A picnic menu only", "A theater seat", "A culinary recipe"], 0, "年底選擇合併夥伴。"),
            ],
        },
        "grammar": {
            "focus": "綜合商務文法",
            "tip": "併購句常考 once / although / to merge with；先確定時間從句與不定詞目的。",
            "questions": [
                _q("Management will announce the plan once parties _____ it.", ["accept", "accepts", "accepting", "accepted"], 0, "複數 parties → accept。"),
                _q("The firm plans _____ away from a strong competitor.", ["to relocate", "relocating", "relocate", "relocated"], 0, "plan to + V。"),
                _q("Employees contribute carefully so they do not _____ files.", ["misplace", "misplacing", "misplaced", "misplaces"], 0, "do not + 原形。"),
                _q("They will select a partner _____ merge with.", ["to", "for", "at", "by"], 0, "to merge with。"),
                _q("Few could _____ the expansion before it was announced.", ["foresee", "forecasted", "foreseen", "foreseeing"], 0, "could + 原形 foresee。"),
            ],
        },
    },
    22: {
        "listening": {
            "partFocus": "Part 4",
            "minutes": 40,
            "warmUp": "用 TTS 聽會議活動：議程、投票、共識、延期與主席主持，當成會議主持短講。",
            "externalDrill": "今日外練 Part 4：會議開場／決議短講 3 篇，抓 agenda / unanimous / defer / preside。",
            "shadowTip": "跟讀 unanimous / consensus / constructive，練習會議結語的下沉語調。",
            "questions": [
                _q("What did the guest speaker pass out before the holiday?", ["A handout", "A suitcase", "A sensor", "A mortgage"], 0, "會前發講義。"),
                _q("What caused a lack of coordination?", ["One member tried to refute the agenda", "Everyone agreed instantly", "No meeting was scheduled", "Plants were watered"], 0, "有人反駁議程導致協調不足。"),
                _q("What was required to reach a unanimous decision?", ["Someone to convince the group and build consensus", "Canceling all votes forever", "Ignoring the board", "Deleting the agenda"], 0, "需要說服並建立共識。"),
                _q("What alternative exists if consensus fails?", ["Defer the vote or reschedule", "Fire the entire board immediately", "End all business talk forever", "Ban handouts"], 0, "可延期投票或改期。"),
            ],
        },
        "grammar": {
            "focus": "長句／詞彙陷阱",
            "tip": "unanimous / consensus / defer / preside 易與 similar-looking 字混淆；看空格要名詞還是動詞。",
            "questions": [
                _q("Reaching a _____ decision required full agreement.", ["unanimous", "anonymous", "unanimously", "unity"], 0, "unanimous decision。"),
                _q("Someone needed to build _____ within the group.", ["consensus", "census", "consent", "concert"], 0, "build consensus。"),
                _q("If talks stall, the board may _____ the vote.", ["defer", "prefer", "refer", "infer"], 0, "defer = 延期。"),
                _q("It would be constructive for someone to _____ over the meeting.", ["preside", "president", "presence", "present"], 0, "preside over = 主持。"),
                _q("They usually _____ meetings when more information is needed.", ["reschedule", "schedule", "scheduling", "rescheduled"], 0, "現在習慣用 reschedule。"),
            ],
        },
    },
    23: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 以模考節奏聽表揚活動：報名、研討會、表揚貢獻、差旅報銷與獎金宣布。",
            "externalDrill": "今日 LC Mixed 考試節奏：連續做 Part 1–4 混合卷 40 分鐘，不中斷重播。",
            "shadowTip": "跟讀 reimbursement / commence / outstanding，模擬頒獎司儀速度。",
            "questions": [
                _q("What did the award ceremony application require?", ["Advance registration", "No registration", "Only a fireplace photo", "A factory leak report"], 0, "需事先登記。"),
                _q("Where would the lecture for all staff be hosted?", ["At the learning center", "At the airport only", "In a cave", "On a highway"], 0, "學習中心舉辦講座。"),
                _q("What did the schedule include?", ["A function to honor outstanding contributions", "A plan to cancel teamwork", "A ban on conferences", "A chemical inspection only"], 0, "表揚傑出貢獻的活動。"),
                _q("What was announced by the end of the night?", ["An entry bonus and salary increase", "A factory closure", "A baggage loss", "A fee-structure ban"], 0, "宣布入職獎金與加薪。"),
            ],
        },
        "grammar": {
            "focus": "綜合錯題型",
            "tip": "表揚／活動題常混詞性與介系詞：register in advance、reimbursement for、commence the ceremony。",
            "questions": [
                _q("Participants must register _____ advance.", ["in", "on", "at", "by"], 0, "in advance。"),
                _q("The learning center will host a lecture _____ all staff.", ["for", "to", "at", "by"], 0, "for all staff。"),
                _q("The objective was to _____ the ceremony with excitement.", ["commence", "commencement", "commencing", "commenced"], 0, "to + 原形 commence。"),
                _q("The company will provide _____ for travel expenses.", ["reimbursement", "reimburse", "reimbursing", "reimbursed"], 0, "provide + 名詞 reimbursement。"),
                _q("Staff felt their hard work had finally earned _____.", ["recognition", "recognize", "recognizing", "recognized"], 0, "earn recognition。"),
            ],
        },
    },
    24: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 聽晉升人事：獎項、評估、任命與董事會一致決議晉升最勝任者。",
            "externalDrill": "今日 LC Mixed：鎖定人事／升遷主題 Part 3–4 各 2 組，計時作答。",
            "shadowTip": "跟讀 appraisal / appointed / competent，注意 /ɪd/ 字尾。",
            "questions": [
                _q("Where did he confirm his new job title?", ["Downstairs at the greenhouse and gymnasium area mentioned", "Only at the airport customs", "Only in a laboratory patent office", "Only on a tour bus"], 0, "文中提到下樓到溫室與體育館確認新職稱。"),
                _q("What led management to promote a skilled worker?", ["A positive appraisal and appointment", "A missing suitcase", "A buffet complaint", "A chemical leak"], 0, "正面考評後被任命並晉升。"),
                _q("What did he consider regarding his role?", ["Whether to resign", "Whether to ban meetings", "Whether to close the bank", "Whether to cancel insurance"], 0, "他考慮是否辭職。"),
                _q("What decision did the board reach?", ["A unanimous decision to promote the most competent candidate", "A decision to fire everyone", "A decision to end appraisals", "A decision to ignore awards"], 0, "一致決議晉升最勝任者。"),
            ],
        },
        "grammar": {
            "focus": "陷阱選項",
            "tip": "promote / promotion、appoint / appointment、competent / competence — 陷阱常是正確詞的其他詞性。",
            "questions": [
                _q("He was _____ after a positive appraisal.", ["appointed", "appointment", "appointing", "appoint"], 0, "被動 was appointed。"),
                _q("Management decided to _____ a skilled worker.", ["promote", "promotion", "promotional", "promoter"], 0, "to + 原形 promote。"),
                _q("The board reached a _____ decision.", ["unanimous", "unanimously", "unanimity", "anonymous"], 0, "形容詞 unanimous。"),
                _q("They promoted the most _____ candidate.", ["competent", "competence", "competently", "competition"], 0, "形容詞 competent。"),
                _q("He considered whether to _____ his role.", ["resign", "resignation", "resigned", "resigning"], 0, "whether to + V。"),
            ],
        },
    },
    25: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 聽通勤文章：計程車、加油站、塞車改道、許可證與修車費用，訓練交通場景關鍵詞。",
            "externalDrill": "今日 LC Mixed：交通廣播＋通勤對話混合練習 40 分鐘。",
            "shadowTip": "跟讀 congestion / detour / malfunction，把子音叢唸清楚。",
            "questions": [
                _q("What did he call instead of using a car rental?", ["A cab", "A banquet chef", "A patent lawyer", "A stockbroker"], 0, "叫計程車而非租車。"),
                _q("How did drivers try to save fuel amid congestion?", ["By taking a detour", "By ignoring all routes", "By deleting permits", "By closing the garage"], 0, "改道以節省燃油。"),
                _q("What problem did the malfunction cause?", ["The car lacked a valid permit for transportation", "The car gained unlimited fuel", "The subway closed forever", "The crosswalk disappeared"], 0, "故障導致缺乏有效運輸許可。"),
                _q("What did he need before heading out to drive?", ["To pay an expense and trust the mechanic", "To cancel the commute", "To merge two companies", "To host a lecture"], 0, "需付費並信任技師。"),
            ],
        },
        "grammar": {
            "focus": "綜合錯題型",
            "tip": "交通題常考 instead of + V-ing、by + V-ing、lack + 名詞。",
            "questions": [
                _q("He called a cab instead of _____ the car rental service.", ["using", "use", "used", "uses"], 0, "instead of + V-ing。"),
                _q("Drivers took a detour _____ save fuel.", ["to", "for", "at", "by"], 0, "to + V 表目的。"),
                _q("Traffic congestion forced drivers to _____ delays.", ["alleviate", "alleviation", "alleviating", "alleviated"], 0, "to + 原形。"),
                _q("The car lacked a valid _____ for transportation.", ["permit", "permissioned", "permitting", "permeate"], 0, "名詞 permit。"),
                _q("He had to pay an expense before he could _____ out.", ["head", "heading", "headed", "heads"], 0, "could + 原形 head。"),
            ],
        },
    },
    26: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 聽銀行帳戶：開戶、自動扣款、逾期通知、對帳單與提領。抓財務關鍵句即可。",
            "externalDrill": "今日 LC Mixed：銀行櫃檯對話＋帳戶通知短講，各練習兩輪。",
            "shadowTip": "跟讀 delinquent / overdue / withdrawal，注意 /d/ /t/ 字尾。",
            "questions": [
                _q("What did he want to do at the bank?", ["Open an account and check his balance", "Book a theater seat", "Ship perishable meat", "Host an award banquet"], 0, "開戶並查餘額。"),
                _q("What kind of notice did the bank send?", ["A delinquent notice about an overdue account", "A concert invitation only", "A factory renovation plan", "A weather alert only"], 0, "逾期帳戶催繳通知。"),
                _q("What did the account statement investigation reveal?", ["A withdrawal amount was due but not yet processed", "The account had unlimited free cash forever", "No deposits ever occurred", "Passwords were unnecessary"], 0, "有一筆提領金額到期但尚未處理。"),
                _q("What payment method was he using at this point?", ["Automatic payment", "Only cash in a jar forever", "Only cryptocurrency mining", "Only traveler's checks from 1900"], 0, "使用自動付款。"),
            ],
        },
        "grammar": {
            "focus": "陷阱選項",
            "tip": "interest / interesting、due / dew、balance 作名詞；陷阱常放形容詞或動詞原形。",
            "questions": [
                _q("He wanted to open an _____ at the bank.", ["account", "accountant", "accounting", "accountable"], 0, "open an account。"),
                _q("The bank sent a notice about an _____ account.", ["overdue", "overdo", "overlook", "overcome"], 0, "overdue = 逾期。"),
                _q("Customers should avoid unnecessary _____.", ["charges", "chargers", "charging", "charged"], 0, "名詞 charges = 費用。"),
                _q("The statement showed a _____ that had not been processed.", ["withdrawal", "withdraw", "withdrew", "withdrawing"], 0, "名詞 withdrawal。"),
                _q("She needed a document proving her spending was _____ logged.", ["successfully", "successful", "success", "succeed"], 0, "副詞 successfully 修飾 logged。"),
            ],
        },
    },
    27: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 聽投資組合：導師建議、獲利、代客購產、股東信任與債券貶值風險。",
            "externalDrill": "今日 LC Mixed：投資顧問對話＋市場短講混合練習。",
            "shadowTip": "跟讀 lucrative / portfolio / depreciation / yield，用冷靜語氣讀風險句。",
            "questions": [
                _q("Why did he listen to his mentor?", ["He worried the joint investment might be fake and needed guidance", "He wanted a free buffet only", "He needed a customs form", "He was booking a gallery ticket"], 0, "擔心投資可能有假，故聽取導師意見。"),
                _q("What did the investment prove to be?", ["Lucrative, with a foreseeable gain", "Completely worthless only", "Illegal forever", "Unrelated to markets"], 0, "投資獲利且可預見收益。"),
                _q("What was required when buying property for a client?", ["A formal lease backed by a sponsor", "Only a picnic basket", "Only a theater handout", "Only a subway map"], 0, "正式租約並有贊助人支持。"),
                _q("What worried conservative investors?", ["Bond depreciation and rapid yield changes", "A missing dessert", "A printer paper jam", "A dress-code memo"], 0, "債券貶值與殖利率急變。"),
            ],
        },
        "grammar": {
            "focus": "綜合錯題型",
            "tip": "on behalf of、consult for advice、lucrative 是投資高頻；注意名詞／形容詞陷阱。",
            "questions": [
                _q("Buying property _____ of a client required a formal lease.", ["on behalf", "in behalf", "for behalf", "at behalf"], 0, "on behalf of。"),
                _q("The investment proved _____.", ["lucrative", "lucre", "lucratively", "lubricate"], 0, "prove + 形容詞。"),
                _q("They consulted a mentor _____ advice.", ["for", "to", "at", "by"], 0, "consult … for advice。"),
                _q("Bond _____ worried conservative investors.", ["depreciation", "depreciate", "depreciating", "depreciated"], 0, "名詞 depreciation 作主詞。"),
                _q("He eventually convinced a shareholder to _____ the outlook.", ["trust", "trusts", "trusted", "trusting"], 0, "to + 原形 trust。"),
            ],
        },
    },
    28: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 以考試節奏聽房產裝修：地板、屋頂、供暖、延遲與承包商維護計畫。本日指定 LC Mixed。",
            "externalDrill": "今日 LC Mixed 全真節奏：連續 40 分鐘混合題，休息只在整段結束後。",
            "shadowTip": "跟讀 remodeling / renovation / densely，保持長句不斷氣練習。",
            "questions": [
                _q("What systems or areas were upgraded or replaced?", ["The floor, frame, garage furniture, and lobby heating", "Only a passport printer", "Only a bank vault", "Only an airplane seat"], 0, "更換地板與框架、加家具並升級大廳供暖。"),
                _q("What did workers repair during remodeling?", ["The rooftop and cleaned the water tank on the veranda", "Only a credit card machine", "Only a merger contract", "Only a survey chart"], 0, "修屋頂並清理阳台水箱。"),
                _q("How did the furnished residence feel after renovation?", ["Spacious, with new drapes in a once unoccupied room", "Smaller and empty of light", "Unrelated to residents", "Closed to all neighbors"], 0, "裝修後寬敞，窗簾覆蓋曾空置房間。"),
                _q("Where is the property located relative to the park?", ["Adjacent to the park", "Inside a laboratory", "On an airplane wing", "Under the ocean only"], 0, "鄰近公園。"),
            ],
        },
        "grammar": {
            "focus": "陷阱選項",
            "tip": "reside / residence / residential；delay / delayed — 看空格要動詞、名詞還是形容詞。",
            "questions": [
                _q("It was appropriate to expect a _____.", ["delay", "delayed", "delaying", "delays"], 0, "expect a delay。"),
                _q("Residents who _____ this urban area appreciate the upgrades.", ["inhabit", "inhabitant", "inhabiting", "inhabited"], 0, "關係子句動詞 inhabit。"),
                _q("The furnished _____ felt spacious after renovation.", ["residence", "reside", "resident", "residing"], 0, "名詞 residence。"),
                _q("The contractor plans to develop and _____ the site.", ["maintain", "maintenance", "maintaining", "maintained"], 0, "to develop and maintain。"),
                _q("The property is _____ to the park.", ["adjacent", "adjacency", "adjacently", "adjust"], 0, "be adjacent to。"),
            ],
        },
    },
    29: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 聽環保文章：污染源、資源節約、回收與霧霾；抓主旨句，略過雜訊詞。",
            "externalDrill": "今日 LC Mixed：環保公告＋社區會議對話混合練。",
            "shadowTip": "跟讀 contamination / conserve / recycling / emission，把科學詞唸準。",
            "questions": [
                _q("What caused unusual weather patterns according to the text?", ["A southern temperature shift linked to contamination", "A bookstore celebration only", "A job fair schedule", "A banquet reservation"], 0, "南方氣溫變化與污染來源相關。"),
                _q("What did conservation efforts aim to improve?", ["Less waste and better recycling disposal", "More factory leaks", "Higher smog only", "Fewer forecasts"], 0, "減少浪費並改善回收處理。"),
                _q("What worried residents by season's end?", ["Rising pollutant emissions and dense smog", "Missing dessert spoons", "A lost boarding pass", "An unpaid banquet tip"], 0, "污染物排放上升與濃霧。"),
                _q("What weather-related risks were mentioned besides pollution?", ["Dust, a possible flood, and windy conditions", "Only tax-free shopping", "Only installment plans", "Only patent filings"], 0, "揚塵、可能淹水與強風。"),
            ],
        },
        "grammar": {
            "focus": "綜合錯題型",
            "tip": "conserve / preserve、dispose of、emission / emit — 環保題高頻詞性轉換。",
            "questions": [
                _q("Efforts to _____ resources can reduce waste.", ["conserve", "conservation", "conservative", "conservatively"], 0, "to + 原形 conserve。"),
                _q("Better ways to _____ of trash include recycling.", ["dispose", "disposal", "disposed", "disposing"], 0, "dispose of。"),
                _q("The source of _____ worried local officials.", ["contamination", "contaminate", "contaminated", "contaminating"], 0, "名詞 contamination。"),
                _q("Rising pollutant _____ created dense smog.", ["emissions", "emit", "emitting", "emitted"], 0, "名詞 emissions。"),
                _q("It is ideal to _____ the land from further damage.", ["preserve", "preservation", "preserving", "preserved"], 0, "to + 原形 preserve。"),
            ],
        },
    },
    30: {
        "listening": {
            "partFocus": "LC Mixed",
            "minutes": 40,
            "warmUp": "用 TTS 聽健康醫療終章：就診、處方、手術與預防計畫；當成考前最後一輪聽力暖身。",
            "externalDrill": "今日 LC Mixed 考前總複習：完整聽力計時模考一段，錯題只複習選項陷阱類型。",
            "shadowTip": "跟讀 prescribed / examination / susceptibility，用沉穩語氣讀醫療說明。",
            "questions": [
                _q("Why did the patient visit a medical facility?", ["For a checkup and injection after feeling sick", "To buy theater tickets", "To merge companies", "To ship cargo"], 0, "感到不適後去做檢查與注射。"),
                _q("What did the physician prescribe a remedy for?", ["His stomach ache and overall wellbeing", "A factory renovation", "A marketing survey", "A parking permit"], 0, "針對胃痛與整體健康開立療法。"),
                _q("What did the comprehensive examination recommend?", ["Periodic dental and dietary checks", "Canceling insurance forever", "Ignoring nutrition", "Skipping recovery"], 0, "建議定期牙科與飲食檢查。"),
                _q("What did he join by the end of recovery?", ["A prevention program", "A cargo shipping crew", "A bookstore campaign only", "A customs inspection team"], 0, "加入預防計畫。"),
            ],
        },
        "grammar": {
            "focus": "陷阱選項",
            "tip": "prescribe / prescription、conscious / consciousness、prevent / prevention — 最後一天專攻詞性陷阱。",
            "questions": [
                _q("The physician _____ a remedy for his stomachache.", ["prescribed", "prescription", "prescribing", "prescriptive"], 0, "過去式動詞 prescribed。"),
                _q("He decided to visit a medical facility for a _____.", ["checkup", "check", "checking", "checked"], 0, "for a checkup。"),
                _q("The healing process required a simple _____.", ["operation", "operate", "operating", "operated"], 0, "名詞 operation。"),
                _q("He joined a _____ program after recovery.", ["prevention", "prevent", "preventing", "prevented"], 0, "prevention program。"),
                _q("Better nutrition can reduce _____ to future illness.", ["susceptibility", "susceptible", "susceptibly", "suspect"], 0, "名詞 susceptibility。"),
            ],
        },
    },
}


def validate_enrichment() -> None:
    assert len(ENRICHMENT) == 30, len(ENRICHMENT)
    for day in range(1, 31):
        e = ENRICHMENT[day]
        assert e["listening"]["partFocus"] == part_focus_for(day), (day, e["listening"]["partFocus"], part_focus_for(day))
        assert e["grammar"]["focus"] == grammar_focus_for(day), (day, e["grammar"]["focus"], grammar_focus_for(day))
        assert e["listening"]["minutes"] == 40
        assert len(e["listening"]["questions"]) == 4
        assert len(e["grammar"]["questions"]) == 5
        for q in e["listening"]["questions"] + e["grammar"]["questions"]:
            assert len(q["choices"]) == 4
            assert 0 <= q["answer"] <= 3


if __name__ == "__main__":
    validate_enrichment()
    print("OK: 30 days, listening×4, grammar×5 each")
    print("Day1 partFocus:", ENRICHMENT[1]["listening"]["partFocus"])
    print("Day1 grammar focus:", ENRICHMENT[1]["grammar"]["focus"])
