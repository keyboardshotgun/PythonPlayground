import os
import re
from tkinter import *
from tkinter import ttk
import tkinter.font as tk_font
import random
import json
import tkinter.messagebox as mbox
import shutil
from bs4 import BeautifulSoup
import requests
import os

# from math import *
q_list = []
r_list = []
f_list = []

# 현재 작업의 path => print(os.getcwd())
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = BASE_DIR + "\\"
EXCEPTLIST = ["ETC-0-A", "ETC-1-A", "#INFO", "문제풀이"]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63"}


def startInit():
    with open(WORK_DIR + "quest_list.json", "rb") as JsonF:
        global q_list
        global r_list
        global f_list
        tempJson = json.load(JsonF)
        q_list = tempJson['data']
        f_list = tempJson['favor']
        r_list = list()

        for entry in q_list:
            if str(entry['ID']) not in EXCEPTLIST and EXCEPTLIST[3] not in str(entry['Description']):
                r_list.append(entry)


class MyApp:

    def __init__(self, parent, question_list):
        self.collectAnswerIndex = 0
        self.collectQuestionIndex = 0
        self.TextBreakLinesEvery = 80
        self.questionList = question_list
        self.combo_str = None
        self.location_combo = None
        self.font8 = tk_font.Font(family="맑은 고딕", size=8)
        self.font10 = tk_font.Font(family="맑은 고딕", size=10)
        self.Font10 = tk_font.Font(family="맑은 고딕", size=11, weight="bold")
        self.font12 = tk_font.Font(family="맑은 고딕", size=12)
        self.categoryList = self.makeCategory()  # 전체 문제 리스트
        self.selectedQuestionList = self.questionList  # 실제 문제제출 용 리스트
        self.previewIndex = 0
        self.btnColor = "#4AD295"
        self.btnActColor = "#339167"
        self.savebtnColor = "#d27e4a"
        self.savebtnActColor = "#7d4b2c"
        self.scrollBarB = None
        self.conBox = None

        # relief option => flat, groove, raised, ridge, solid, sunken
        # 프레임 시작
        self.frameA = LabelFrame(root, text="Menu", relief="groove")
        # 회차선택
        self.makeCategoryElement()
        # Start Button
        self.startBtn = Button(self.frameA, text="시작", command=self.startQuestion,
                               width=12, height=1, relief="groove", fg="white", bg=self.btnColor, font=self.Font10
                               , activebackground=self.btnActColor, activeforeground="#1e573e", overrelief="ridge"
                               ).pack(side=LEFT, padx=5)

        self.reloadBtn = Button(self.frameA, text="Reload(소스)", command=self.readSourceAgain
                                , width=12, height=1, relief="groove", fg="white", bg=self.btnColor, font=self.Font10
                                , activebackground=self.btnActColor, activeforeground="#1e573e", overrelief="ridge"
                                ).pack(side=LEFT, padx=5)

        self.resetBtn = Button(self.frameA, text="초기화", command=self.readSourceAgain
                               , width=12, height=1, relief="groove", fg="white", bg=self.btnColor, font=self.Font10
                               , activebackground=self.btnActColor, activeforeground="#1e573e", overrelief="ridge"
                               ).pack(side=LEFT, padx=5)

        self.loadFavorBtn = Button(self.frameA, text="즐찾풀기", command=self.favorToQuesitons
                                   , width=12, height=1, relief="groove", fg="white", bg=self.btnColor, font=self.Font10
                                   , activebackground=self.btnActColor, activeforeground="#1e573e", overrelief="ridge"
                                   ).pack(side=LEFT, padx=5)

        self.getWebNewWordBtn = Button(self.frameA, text="웹신규", command=self.addNewKeywordFromWeb
                                       , width=8, height=1, relief="groove", fg="white", bg=self.btnColor,
                                       font=self.Font10
                                       , activebackground=self.btnActColor, activeforeground="#1e573e",
                                       overrelief="ridge"
                                       ).pack(side=LEFT, padx=5)

        self.searchBtn = Button(self.frameA, text="사전검색", command=self.searchEngine
                                , width=6, height=1, relief="groove", fg="white", bg=self.btnColor, font=self.Font10
                                , activebackground=self.btnActColor, activeforeground="#1e573e", overrelief="ridge"
                                ).pack(side=RIGHT, padx=5)

        self.webSearchBtn = Button(self.frameA, text="웹검색", command=self.webSearchEngine
                                   , width=6, height=1, relief="groove", fg="white", bg=self.btnColor, font=self.Font10
                                   , activebackground=self.btnActColor, activeforeground="#1e573e", overrelief="ridge"
                                   ).pack(side=RIGHT, padx=5)

        # Search Input
        self.searchInput = Entry(self.frameA, width=20, borderwidth=6, relief='flat', justify=LEFT)
        self.searchInput.bind('<Return>', self.enterCallBack)  # 검색 엔터키 바인딩
        self.searchInput.pack(side=RIGHT)  # self.searchInput.delete(0, END)

        # 입력단 프레임
        self.frameE = LabelFrame(root, text="New Question")
        self.makeCateInput = Entry(self.frameE, width=20, borderwidth=6, relief='flat', justify=LEFT)
        self.makeAnswerInput = Entry(self.frameE, width=20, borderwidth=6, relief='flat', justify=LEFT)

        self.questionInputLabelFrame = LabelFrame(self.frameE, text="")
        Label(self.questionInputLabelFrame, text="문\n제\n입\n력", width=3, height=5, fg="#333333", bg="#DDDDDD",
              relief="groove").pack(side=LEFT)

        self.questionInpuBottomFrame = Frame(self.questionInputLabelFrame, width=900)

        self.makeModifyBtn = Button(self.questionInpuBottomFrame, text="수정저장", command=self.modifyQuestion
                                    , width=10, height=1, relief="groove", fg="white", bg=self.savebtnColor,
                                    font=self.Font10
                                    , activebackground=self.savebtnActColor, activeforeground="#1e573e",
                                    overrelief="ridge")
        self.makeModifyBtn.pack(side=RIGHT, pady=5, padx=10)

        self.makeSaveBtn = Button(self.questionInpuBottomFrame, text="신규저장", command=self.addNewQuestion
                                  , width=10, height=1, relief="groove", fg="white", bg=self.savebtnColor,
                                  font=self.Font10
                                  , activebackground=self.savebtnActColor, activeforeground="#1e573e",
                                  overrelief="ridge")
        self.makeSaveBtn.pack(side=RIGHT, pady=5)

        self.questionInpuBottomFrame.pack(side=BOTTOM, fill=BOTH)

        self.makeSaveQuestionInput = Entry(self.questionInputLabelFrame, width=130, borderwidth=8, relief='flat',
                                           justify=LEFT, font=self.font10)
        self.makeSaveQuestionInput.pack(side=BOTTOM, fill='y')
        self.questionInputLabelFrame.pack(side=BOTTOM, padx=5, pady=10, fill=BOTH)

        Label(self.frameE, text="카테고리", width=10, height=1, fg="#333333", bg="#DDDDDD", relief="groove").pack(side=LEFT,
                                                                                                              padx=15,
                                                                                                              pady=5,
                                                                                                              fill=BOTH)

        self.makeCateInput.pack(side=LEFT)
        Label(self.frameE, text="답변입력", width=10, height=1, fg="#333333", bg="#DDDDDD", relief="groove").pack(side=LEFT,
                                                                                                              padx=15,
                                                                                                              pady=5,
                                                                                                              fill=BOTH)
        self.makeAnswerInput.pack(side=LEFT)

        Label(self.frameE, text="전체 데이터 조회(" + str(len(q_list) - 1) + ")", width=20, height=2,
              fg="#333333", bg="#DDDDDD", relief="groove"
              ).pack(side=LEFT, padx=15, pady=5, fill=BOTH)

        self.previewDeleteBtn = Button(self.frameE, text="삭제", command=lambda: self.arrowControl('DELETE')
                                       , width=4, height=1, relief="groove", fg="white", bg=self.savebtnColor,
                                       font=self.Font10
                                       , activebackground=self.savebtnActColor, activeforeground="#1e573e",
                                       ).pack(side=RIGHT, padx=5)

        self.previewModifyBtn = Button(self.frameE, text="로드", command=lambda: self.arrowControl('MODIFY')
                                       , width=8, height=1, relief="groove", fg="white", bg=self.savebtnColor,
                                       font=self.Font10
                                       , activebackground=self.savebtnActColor, activeforeground="#1e573e",
                                       ).pack(side=RIGHT)

        self.previewNextBtn = Button(self.frameE, text=">", command=lambda: self.arrowControl('NEXT')
                                     , width=3, height=1, relief="groove", fg="#333333", bg='white', font=self.Font10
                                     , activebackground="#d5d5d5", overrelief="ridge"
                                     ).pack(side=RIGHT, padx=5)

        # self.previewLabel = Label(self.frameE, text="", width=4, height=2, fg="#333333", bg="#f5f5f5", relief="flat")
        # self.previewLabel.pack(side=RIGHT)

        self.showInputIndex = Entry(self.frameE, width=4, borderwidth=5, relief='flat', justify=CENTER, font=self.font8)
        self.showInputIndex.pack(side=RIGHT)

        self.previewPrevBtn = Button(self.frameE, text="<", command=lambda: self.arrowControl('PREV')
                                     , width=3, height=1, relief="groove", fg="#333333", bg='white',
                                     font=self.Font10
                                     , activebackground="#d5d5d5", overrelief="ridge"
                                     ).pack(side=RIGHT, padx=5)

        # 정보 메세지 및 문제 프레임
        # relief option => flat, groove, raised, ridge, solid, sunken
        self.frameB = LabelFrame(root, text="문제")
        self.message_total_text = StringVar()
        self.message_total_text.set(str(len(self.selectedQuestionList)) + " 문제")
        self.message_question_text = StringVar()
        self.message_question_text.set("정보처리 기사 2013 - 2020 실기 기출 문제")
        self.message_result_text = StringVar()
        self.message_result_text.set("100점만에 몇 점?")

        self.message_total = Message(self.frameB, relief="ridge", textvariable=self.message_total_text,
                                     font=self.font8, width=40
                                     , fg="#333333", bg="#DDDDDD"
                                     )

        self.favorCheckVar = BooleanVar()
        # self.favorCheckVar.set(False)
        self.favorCheckbutton = Checkbutton(self.frameB, text="즐겨찾기", var=self.favorCheckVar
                                            , fg="black", bg="#00ddff", selectcolor="white"
                                            , relief="ridge", overrelief="groove"
                                            , activeforeground="red", command=self.toggleCheckBtn)  #

        self.message_total.pack(side=LEFT, padx=5, pady=5, fill=BOTH)
        self.favorCheckbutton.pack(side=BOTTOM, padx=5, pady=5, anchor=SE)

        self.message_question = Message(self.frameB, relief="sunken", textvariable=self.message_question_text,
                                        font=self.Font10
                                        , fg="#333333", bg="#FFFFFF", width=900, justify=LEFT
                                        )

        self.message_question.pack(side=LEFT, padx=5, pady=5, fill=BOTH, expand=True, ipady=10)

        self.frameC = LabelFrame(root, text="결과창")
        self.message_result = Message(self.frameC, relief="groove", textvariable=self.message_result_text
                                      , font=self.font12
                                      , fg="#333333", bg="#FFFFFF", width=900, justify=LEFT
                                      )
        self.message_result.pack(fill=BOTH, padx=5, pady=5, expand=True, ipady=10)

        # 선택지 / 검색결과 출력단 프레임
        self.frameD = LabelFrame(root, text="화이팅")
        self.scrollBarB = Scrollbar(self.frameD)
        self.scrollBarB.pack(side="right", fill="y")
        self.conBox = Text(self.frameD, yscrollcommand=self.scrollBarB.set, width=1150, height=70, wrap=WORD,
                           font=self.font10)
        self.conBox.pack(side="left", fill="both", expand=True, ipadx=5, ipady=5, padx=5, pady=5)
        self.scrollBarB.config(command=self.conBox.yview)

        self.frameA.pack(fill=BOTH, padx=5, pady=10)  # 메뉴
        self.frameE.pack(fill=BOTH, padx=5, pady=10)  # 신규 문제 작성
        self.frameB.pack(fill=BOTH, padx=5, pady=10, ipadx=5, ipady=5)  # 문제 출제 프레임
        self.frameC.pack(fill=BOTH, padx=5, pady=10, ipadx=5, ipady=5)  # 문제 보기 리스트
        self.frameD.pack(fill=BOTH, padx=5, pady=10)
        self.refreshPreviewLabelNumber()
        # self.seperatorD = Frame(root, width=1200, height=20, bd=1, relief='flat').pack(fill=BOTH)  # 분리선
        # self.frameB.pack_propagate(0)  # 크기고정용

    def testJson(self, addordel):
        global f_list
        with open(WORK_DIR + "quest_list.json", "r", encoding='UTF-8') as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
            favorNo = q_list[int(self.showInputIndex.get())]['No']
            oldSet = set(jsonObject['favor'])
            if addordel == 'add':
                oldSet.add(str(favorNo))
            elif addordel == 'remove':
                if str(favorNo) in oldSet:
                    oldSet.remove(str(favorNo))

            jsonObject['favor'] = list(oldSet)
            f_list = jsonObject['favor']

        with open(WORK_DIR + "quest_list.json", "w", encoding='UTF-8') as fp:
            json.dump(jsonObject, fp, ensure_ascii=False, indent=2)
            fp.truncate()
            fp.close()
            # self.readSourceAgain()

    def toggleCheckBtn(self):
        if self.favorCheckVar.get() is True:
            self.testJson('add')
        else:
            self.testJson('remove')

    def enterCallBack(self, event):
        self.searchEngine()

    def refreshPreviewLabelNumber(self):
        # self.previewLabel.configure(text=str(self.previewIndex))
        # self.previewLabel.update()
        self.showInputIndex.delete(0, END)
        self.showInputIndex.insert(0, str(self.previewIndex))
        self.showInputIndex.update()
        ID = q_list[self.previewIndex]['ID']
        # Word = q_list[self.previewIndex]['Word']
        Description = q_list[self.previewIndex]['Description']
        oldNo = q_list[self.previewIndex]['No']
        previewQuestion = "[" + ID + "]\t" + '\n\n' + Description
        self.message_question_text.set(previewQuestion)
        self.isFavorQuestion(oldNo)

    def setModifyTarget(self):
        if int(self.showInputIndex.get()) != int(self.previewIndex):
            self.previewIndex = int(self.showInputIndex.get())

        tempData = q_list[self.previewIndex]
        self.makeCateInput.delete(0, END)
        self.makeAnswerInput.delete(0, END)
        self.makeSaveQuestionInput.delete(0, END)
        self.makeCateInput.insert(0, tempData['ID'])
        self.makeAnswerInput.insert(0, tempData['Word'])
        self.makeSaveQuestionInput.insert(0, tempData['Description'])

    def arrowControl(self, controls):
        if controls == 'PREV':
            if self.previewIndex <= 0:
                self.previewIndex = len(q_list) - 1
            else:
                self.previewIndex = self.previewIndex - 1

            self.refreshPreviewLabelNumber()
        elif controls == 'NEXT':
            if self.previewIndex >= len(q_list) - 1:
                self.previewIndex = 0
            else:
                self.previewIndex = self.previewIndex + 1

            self.refreshPreviewLabelNumber()
        elif controls == 'MODIFY':
            self.setModifyTarget()
        elif controls == 'DELETE':
            self.deleteQuestion()
        else:
            return False

    def deleteQuestion(self):
        if self.previewIndex is not None:
            confirm = mbox.askyesno("알림", "해당 문제를 삭제 하시겠습니까?\n삭제 후 복구 되지 않습니다.")
            if confirm is True:
                q_list.pop(self.previewIndex)
                self.updateOrAddJsonFile()
                self.message_question_text.set("")

    def modifyQuestion(self):
        global q_list
        thisCate = self.makeCateInput.get()
        thisAnswer = self.makeAnswerInput.get()
        thisQuesiton = self.makeSaveQuestionInput.get()
        checkModify = False

        if len(thisCate) < 1:
            mbox.showerror('카테고리문제', '카테고리가 없습니다.')
            return False

        if len(thisAnswer) < 1:
            mbox.showerror('답변문제', '답변을 입력해 주세요')
            return False

        if len(thisQuesiton) < 1:
            mbox.showerror('질문문제', '질문을 입력해 주세요')
            return False

        ID = q_list[self.previewIndex]['ID'].strip()
        Word = q_list[self.previewIndex]['Word'].strip()
        Description = q_list[self.previewIndex]['Description'].strip()

        if "\\n" in thisQuesiton:
            thisQuesiton = thisQuesiton.replace("\\n", "\n")

        if thisCate.strip() != ID:
            q_list[self.previewIndex]['ID'] = thisCate
            checkModify = True

        if thisAnswer.strip() != Word:
            q_list[self.previewIndex]['Word'] = thisAnswer
            checkModify = True

        if Description.strip() != thisQuesiton:
            q_list[self.previewIndex]['Description'] = thisQuesiton
            checkModify = True

        if checkModify is True:
            self.updateOrAddJsonFile()
            self.refreshPreviewLabelNumber()

    def addNewQuestion(self):
        global q_list
        dummyCate = self.categoryList[1]  # 전체목록 다음 것을 가져온다.
        thisNumber = len(q_list) + 1
        thisCate = self.makeCateInput.get() or dummyCate  # 카테고리 입력이 없으면 최신것으로 자동입력
        thisAnswer = self.makeAnswerInput.get()
        thisQuesiton = self.makeSaveQuestionInput.get()

        if len(thisAnswer) < 1:
            mbox.showerror('답변문제', '답변을 입력해 주세요')
            return False

        if len(thisQuesiton) < 1:
            mbox.showerror('질문문제', '질문을 입력해 주세요')
            return False

        addDict = {"No": thisNumber, "ID": thisCate, "Feq": 1, "Word": thisAnswer, "Description": thisQuesiton}
        q_list.append(addDict)
        self.updateOrAddJsonFile()

    def updateOrAddJsonFile(self):
        global q_list
        global f_list

        for index, entry in enumerate(q_list):
            entry['No'] = index + 1

        OriginFilePath = WORK_DIR + 'quest_list.json'
        BakupFilePath = WORK_DIR + 'quest_list.bak'
        if os.path.isfile(WORK_DIR + 'quest_list.json'):
            shutil.copyfile(OriginFilePath, BakupFilePath)
        with open(WORK_DIR + "quest_list.json", "w", encoding='UTF-8') as fp:
            json.dump({"data": q_list, "favor": f_list}, fp, ensure_ascii=False, indent=2)
            fp.truncate()
            fp.close()
        self.readSourceAgain()

    def makeCategoryElement(self):
        self.combo_str = StringVar()
        if not isinstance(self.location_combo, ttk.Combobox):  # <class 'tkinter.ttk.Combobox'>
            self.location_combo = ttk.Combobox(self.frameA, height=60, width=20, textvariable=self.combo_str,
                                               state="readonly")
            self.location_combo.bind("<<ComboboxSelected>>", self.makeQuestionList)
            self.location_combo.pack(side=LEFT, padx=10, pady=10)

        self.location_combo.set("회차 선택")
        self.location_combo['values'] = self.categoryList
        self.location_combo.current(0)

    def readSourceAgain(self):
        global r_list
        startInit()
        self.questionList = r_list
        self.selectedQuestionList = r_list
        self.message_total_text.set(str(len(self.selectedQuestionList)) + " 문제")
        self.categoryList = self.makeCategory()
        self.location_combo.set('')
        self.makeCategoryElement()
        self.makeAnswerInput.delete(0, END)
        self.makeSaveQuestionInput.delete(0, END)
        self.frameA.update()
        self.frameB.update()
        self.frameE.update()
        self.frameD.update()

    def makeCategory(self) -> list:
        category_temp = {'전체목록'}
        for ent in self.questionList:
            category_temp.add(ent['ID'])
        ret = list(category_temp)
        ret.sort(reverse=True)
        return ret

    def favorToQuesitons(self):
        global f_list
        if len(f_list) > 0:
            self.selectedQuestionList = list()

            for ent in self.questionList:
                if str(ent['No']) in f_list:
                    self.selectedQuestionList.append(ent)

            self.message_total_text.set(str(len(self.selectedQuestionList)) + " 문제")
            self.frameB.update()
            self.startQuestion()
        else:
            mbox.showinfo('알림', '즐겨찾기에 저장된 항목이 없습니다.')

    def makeQuestionList(self, event):
        keyCate = self.location_combo.get()
        self.selectedQuestionList = list()
        if keyCate == '전체목록':
            self.selectedQuestionList = self.questionList
        else:
            for ent in self.questionList:
                if ent['ID'] == str(keyCate):
                    self.selectedQuestionList.append(ent)
        self.message_total_text.set(str(len(self.selectedQuestionList)) + " 문제")
        self.frameB.update()
        self.startQuestion()

    def isFavorQuestion(self, oldno):
        if str(oldno) in f_list:
            self.favorCheckVar.set(True)
        else:
            self.favorCheckVar.set(False)

    def resetElements(self):
        self.removeButtons()
        self.collectAnswerIndex = 0
        self.collectQuestionIndex = 0
        self.message_result_text.set("오늘도 즐겁게 기출공부")
        self.frameC.update()

    def startQuestion(self):
        self.resetElements()
        listSize = len(self.selectedQuestionList)
        if listSize > 0:
            selectedIndex = random.randint(1, listSize) - 1  # 1에서 5까지 정수 (1~5)
            self.collectQuestionIndex = selectedIndex
            nowQuestion = "[" + self.selectedQuestionList[selectedIndex]['ID'] + "]" + "\n\n" + \
                          self.selectedQuestionList[selectedIndex]['Description']
            nowAnswer = self.selectedQuestionList[selectedIndex]['Word']
            nowQuestionNo = self.selectedQuestionList[selectedIndex]['No']
            self.showInputIndex.delete(0, END)  # InputIndex Update
            self.showInputIndex.insert(0, str(int(nowQuestionNo) - 1))  # InputIndex Update
            sampleList = random.sample(self.questionList, k=9)
            dummyAnswerList = []
            insertIndex = random.randint(0, 8)
            for (index, ent) in enumerate(sampleList):
                if nowQuestionNo != ent['No']:
                    if insertIndex == index:
                        dummyAnswerList.append(nowAnswer)
                    dummyAnswerList.append(ent['Word'])

            self.message_question_text.set(nowQuestion)
            random.shuffle(dummyAnswerList)

            for (index, e) in enumerate(dummyAnswerList):
                if e == nowAnswer:
                    self.collectAnswerIndex = index
                self.makeAnswerButton(index, e)

            self.isFavorQuestion(nowQuestionNo)
            print('번호:', self.collectAnswerIndex, ' | 답:', nowAnswer)
        else:
            mbox.showinfo('완료', '해당 카테고리의 모든 문제를 풀었습니다.\n새로운 카테고리를 선택해 주세요.')
            # {"No":1 ,"ID":"2020-02-A-1","Feq":1,"Word":"( new ) FunctionName()","Description":"Java 인스턴스 생성 명령어"}

    def checkAnswers(self, e):
        self.message_result_text.set("")
        if self.collectAnswerIndex == e:
            self.message_result_text.set("정답 입니다.")
            self.selectedQuestionList.pop(self.collectQuestionIndex)
            self.message_total_text.set(str(len(self.selectedQuestionList)) + " 문제")
            self.frameB.update()
            self.frameC.update()
            self.startQuestion()
        else:
            self.message_result_text.set("오답 입니다.")
            self.frameC.update()

    def removeButtons(self):
        for widget in self.frameD.winfo_children():
            widget.destroy()
            # self.frameD.pack_forget() 프레임 자체 삭제 명령어

    def makeAnswerButton(self, index, ent):
        btnText = str(index + 1) + "." + " " * 3 + ent
        Button(self.frameD, fg="#333333", bg="#5d9e5d", anchor="w", text=btnText, font=self.Font10,
               command=lambda: self.checkAnswers(index)).pack(side=TOP, fill='x')

    def insertNewlines(self, text) -> str:
        lines = []
        for i in range(0, len(text), self.TextBreakLinesEvery):
            lines.append(text[i:i + self.TextBreakLinesEvery])
        return '\n'.join(lines)

    def webSearchEngine(self):

        search_text = self.searchInput.get().strip()
        if search_text and len(search_text) > 1:

            first_check = ''
            for widget in self.frameD.winfo_children():
                first_check = widget.winfo_class()

            if first_check == 'Button':
                print('버튼이 들어 있네 / 기존 것을 날리자')
                self.resetFrameD()

            #  신규등록데이터 1 - 300
            #  http://terms.tta.or.kr/dictionary/dictionaryNewWordList.do?listPage=1&firstWord=N&word_seq=&listCount=300
            siteUrl = "https://terms.tta.or.kr/dictionary/dictionaryView.do?subject="
            toUrl = siteUrl + search_text
            try:
                res = requests.get(toUrl, headers=headers)
                if res.status_code != 404:
                    soup = BeautifulSoup(res.text, "lxml")
                    motherDiv = soup.find_all("div", id=["cont"])
                    title = ''
                    content = ''

                    for row in motherDiv:
                        title = row.find_all('dt')
                        content = row.find_all("div", class_=["no_css"])

                    if title and content:
                        # 프레임에 정보 넣기
                        word = title[0].text.strip()
                        desc = content[0].text.strip()

                        self.conBox.delete('1.0', END)
                        self.message_result_text.set('')

                        self.message_result_text.set('키워드 웹검색 : ' + word)
                        self.conBox.insert(END, desc)
                        self.conBox.insert(END, '\n\n')
                        self.frameD.update()
                    else:
                        mbox.showinfo('!', '검색 결과가 없습니다.')

            except SyntaxError:
                print("Syntax", 'Syntax 오류 입니다.')
            except ConnectionError:
                print("ConnectionError", 'ConnectionError 오류 입니다.')
        else:
            mbox.showinfo('!', '2자 이상 입력')

    def resetFrameD(self):
        for widget in self.frameD.winfo_children():
            widget.destroy()
        self.scrollBarB = Scrollbar(self.frameD)
        self.scrollBarB.pack(side="right", fill="y")
        self.conBox = Text(self.frameD, yscrollcommand=self.scrollBarB.set, width=1150, height=70, wrap=WORD,
                           font=self.font10)
        self.conBox.pack(side="left", fill="both", expand=True, ipadx=5, ipady=5, padx=5, pady=5)
        self.scrollBarB.config(command=self.conBox.yview)

    def searchEngine(self):
        first_check = ''
        for widget in self.frameD.winfo_children():
            first_check = widget.winfo_class()

        if first_check == 'Button':
            print('버튼이 들어 있네 / 기존 것을 날리자')
            self.resetFrameD()

        # 사전 검색시작
        text = self.searchInput.get().strip()
        self.message_result_text.set('')
        self.conBox.delete('1.0', END)
        tempList = list()
        if len(text) >= 2:

            for qus in q_list:
                if text.lower() in str(qus).lower():
                    aNO = 'No. ' + str(qus['No'] - 1).strip()
                    ID = qus['ID'].strip()
                    Word = qus['Word'].strip()
                    Description = self.insertNewlines(qus['Description'].strip())
                    strText = '(' + aNO + ') ' + ID + '\t[ ' + Word + ' ]\n\n ㄴ> ' + Description
                    tempList.append(strText)
                else:
                    continue

            if len(tempList) > 0:
                self.message_result_text.set('검색완료, 결과 : ' + str(len(tempList)) + '건 있음')
                tempList.sort()
                for index, xty in enumerate(tempList):
                    thisStr = '\n' + str(index + 1) + ') ' + xty
                    self.conBox.insert(END, thisStr)
                    self.conBox.insert(END, '\n\n')

                self.frameD.update()
            else:
                self.message_result_text.set(text + ': 검색결과 없음')
        else:
            mbox.showinfo('알림', "검색어는 2자이상 입력해 주세요")

    def addNewKeywordFromWeb(self):
        #  신규등록데이터 1 - 300
        global q_list
        self.conBox.delete('1.0', END)
        self.message_result_text.set('')
        toUrl = "http://terms.tta.or.kr/dictionary/dictionaryNewWordList.do?listPage=1&firstWord=N&word_seq=&listCount=300"
        tempList = []

        try:
            res = requests.get(toUrl, headers=headers)
            if res.status_code != 404:
                soup = BeautifulSoup(res.text, "lxml")
                motherDiv = soup.find_all("div", id=["m_content"])
                dlLists = None

                for row in motherDiv:
                    dlLists = row.find_all('dl')

                next_q_Index = len(q_list)
                regex = re.compile("\.{3,}")
                desc = ''

                for dl in dlLists:
                    Word = dl.find_all('dt')[0].text.strip()
                    Description = dl.find_all('dd')[0].text.strip()
                    yesOrNo = regex.search(Description)

                    if yesOrNo is not None:  # ... 이 있다.
                        t_array = Description.split('.')[0:-4]  # 신규 등록시 에러가 난다면 여기가 문제다. 끝이 ... 으로 끝나지 않을 수도 있기 때문에...
                        for XT in t_array:
                            desc += XT.strip() + '.\n'
                    else:
                        t_array = Description.split('.')  # ... 이 없다
                        for XT in t_array:
                            desc += XT.strip() + '.\n'

                    next_q_Index = next_q_Index + 1
                    q_list.append({"No": next_q_Index , "ID": "2020-NEW", "Feq": 1, "Word": Word , "Description": desc})
                    strText = '\t[ ' + Word + ' ]\n\n ㄴ> ' + desc
                    tempList.append(strText)
                    desc = ''

                tempList.sort()

                for index, xty in enumerate(tempList):
                    thisStr = '\n' + str(index + 1) + ') ' + xty
                    self.conBox.insert(END, thisStr)
                    self.conBox.insert(END, '\n\n')

                self.message_result_text.set('검색완료, 결과 : ' + str(len(dlLists)) + '건 있음')
                self.updateOrAddJsonFile()

        except SyntaxError:
            print("Syntax", 'Syntax 오류 입니다.')
        except ConnectionError:
            print("ConnectionError", 'ConnectionError 오류 입니다.')


startInit()
root = Tk()
w = 1100  # width for the Tk root
h = 1100  # height for the Tk root
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen
x = 1500  # (ws/2) - (w/2) 가로 중앙공식
y = 50  # (hs/2) - (h/2) 세로 중앙공식
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
rootBackgroundColor = '#F5F5F5'
root.title("정보처리기사 실기 : " + str(len(r_list)) + " 문제")  # 타이틀
root.configure(bg=rootBackgroundColor, padx=10, pady=10)
root.resizable(False, True)
myapp = MyApp(root, r_list)
root.mainloop()
