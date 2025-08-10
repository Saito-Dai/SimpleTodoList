import tkinter as tk
from tkinter import messagebox


class Task:
    """単一のタスクを表すデータ構造。

    属性:
        title (str): タスク名。
        due_date (str): 期日（文字列で保持。厳密な日付は今回は扱わない）。
        priority (str): 優先度（例: High/Medium/Low など、自由入力）。
        is_completed (bool): 完了状態。
    """

    def __init__(self, title, due_date, priority):
        # 必須情報（タイトル・期日・優先度）を受け取り、初期状態は未完了にする
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.is_completed = False

    def __str__(self):
        """Listboxやprint表示用の文字列表現を返す。"""
        status = "Completed" if self.is_completed else "Not Completed"
        return f"{self.title} - {self.due_date} - {self.priority} - {status}"


class TodoList:
    """タスクの集合（一覧）を管理するクラス。追加/編集/削除/状態変更を担当。"""

    def __init__(self):
        # タスクを保持する内部リスト
        self.tasks = []

    def add_task(self, title, due_date, priority):
        """新しいタスクを作成してリストに追加する。"""
        new_task = Task(title, due_date, priority)
        self.tasks.append(new_task)

    def remove_task(self, task_index):
        """指定インデックスのタスクを削除する。範囲外は無視する。"""
        if 0 <= task_index < len(self.tasks):
            self.tasks.pop(task_index)

    def edit_task(self, task_index, title=None, due_date=None, priority=None):
        """指定インデックスのタスク内容を部分的に更新する。"""
        task = self.tasks[task_index]
        if title:
            task.title = title
        if due_date:
            task.due_date = due_date
        if priority:
            task.priority = priority

    def mark_completed(self, task_index):
        """指定タスクを完了にする。"""
        self.tasks[task_index].is_completed = True

    def mark_incomplete(self, task_index):
        """指定タスクを未完了に戻す。"""
        self.tasks[task_index].is_completed = False

    def show_tasks(self):
        """デバッグ用: タスク一覧をコンソールに出力する。"""
        for i, task in enumerate(self.tasks):
            print(f"{i}. {task}")


class TodoApp:
    """TkinterでGUIを構築して、TodoListを操作するアプリケーション。"""

    def __init__(self, root):
        # ルートウィンドウの基本設定
        self.root = root
        self.root.title("Todoリスト")

        # データモデル: タスク一覧
        self.todo_list = TodoList()

        # ---- タイトル（見出し） ----
        self.title_label = tk.Label(root, text="タスク管理アプリ", font=("Helvetica", 16))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # ---- 入力欄（タイトル、期日、優先度）----
        # ラベルとEntryはグリッドで縦に並べる
        self.title_label = tk.Label(root, text="タイトル")  # 変数名は流用しているが機能上は問題なし
        self.title_label.grid(row=1, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.due_date_label = tk.Label(root, text="期日")
        self.due_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.due_date_entry = tk.Entry(root, width=30)
        self.due_date_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        self.priority_label = tk.Label(root, text="優先度")
        self.priority_label.grid(row=3, column=0, padx=5, pady=5)
        self.priority_entry = tk.Entry(root, width=30)
        self.priority_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        # ---- 追加ボタン ----
        self.add_button = tk.Button(root, text="タスク追加", width=20, command=self.add_task)
        self.add_button.grid(row=4, column=0, columnspan=3, pady=10)

        # ---- 一覧表示（Listbox） ----
        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.grid(row=5, column=0, columnspan=3, pady=10)

        # ---- 操作用ボタン群 ----
        # 完了ボタン: 選択されたタスクを完了にする
        self.mark_completed_button = tk.Button(root, text="完了", width=20, command=self.mark_completed)
        self.mark_completed_button.grid(row=6, column=0, pady=10)

        # 削除ボタン: 選択されたタスクを削除する
        self.remove_button = tk.Button(root, text="削除", width=20, command=self.remove_task)
        self.remove_button.grid(row=6, column=1, pady=10)

        # （拡張余地）未完了に戻すボタン等は必要になったら追加可能

    def add_task(self):
        """入力欄の値を読み取り、タスクリストに追加して表示を更新する。"""
        # Entryから現在値を取得
        title = self.title_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_entry.get()

        # 入力バリデーション（どれかが空なら警告）
        if not title or not due_date or not priority:
            messagebox.showwarning("入力エラー", "すべてのフィールドを入力してください")
            return

        # データモデルに追加して、Listboxを最新状態に
        self.todo_list.add_task(title, due_date, priority)
        self.update_task_listbox()

        # 使い勝手向上のため、追加後は入力欄をクリア
        self.title_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)

    def remove_task(self):
        """選択中のタスクを削除して表示更新。選択なしの場合は警告。"""
        try:
            # Listboxの選択インデックスを取得（複数選択は想定しないため先頭のみ）
            selected_task_index = self.task_listbox.curselection()[0]
            self.todo_list.remove_task(selected_task_index)
            self.update_task_listbox()
        except IndexError:
            # 何も選択されていないケース
            messagebox.showwarning("選択エラー", "削除するタスクを選択してください")

    def mark_completed(self):
        """選択中のタスクを完了にして表示更新。選択なしの場合は警告。"""
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.todo_list.mark_completed(selected_task_index)
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("選択エラー", "完了するタスクを選択してください")

    def update_task_listbox(self):
        """内部データ（TodoList.tasks）からListboxの表示を作り直す。"""
        self.task_listbox.delete(0, tk.END)
        for task in self.todo_list.tasks:
            self.task_listbox.insert(tk.END, task)


# エントリーポイント: このファイルを直接実行したときだけGUIを起動する
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
