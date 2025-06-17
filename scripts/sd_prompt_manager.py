import os
import gradio as gr
import yaml
import html
from modules import scripts

css = """
.prompt-button {
    background-color: #FF9800 !important;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 16px;
    margin: 4px;
    cursor: pointer;
    min-width: 100px;
    font-size: 14px;
    transition: background 0.2s;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.prompt-button:hover, .prompt-button:focus {
    background-color: #F57C00;
    outline: none;
}
"""

PROMPT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt_data.yaml")

# --- データ管理関数 ---

def load_prompts():
    prompts_data = {'categories': {}}
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            try:
                loaded_data = yaml.safe_load(f)
                if loaded_data and 'categories' in loaded_data and isinstance(loaded_data['categories'], dict):
                    prompts_data = loaded_data
            except yaml.YAMLError as e:
                print(f"Error loading YAML file '{PROMPT_FILE}': {e}")
    return prompts_data

def save_prompts(prompts_data):
    os.makedirs(os.path.dirname(PROMPT_FILE), exist_ok=True)
    with open(PROMPT_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(prompts_data, f, allow_unicode=True, sort_keys=False)

def get_categories():
    prompts_data = load_prompts()
    categories = prompts_data.get('categories', {})
    category_list = list(categories.keys())
    return category_list

def get_labels_by_category(category):
    prompts_data = load_prompts()
    categories = prompts_data.get('categories', {})
    category_data = categories.get(category, [])
    labels_dict = {}
    for item in category_data:
        if 'label' in item and 'prompt' in item:
            labels_dict[item['label']] = item['prompt']
    return labels_dict

def get_prompt_content(category, label):
    prompts_data = load_prompts()
    category_list = prompts_data.get('categories', {}).get(category, [])
    for item in category_list:
        if item.get('label') == label:
            return item.get('prompt', "")
    return ""

# --- CRUD 操作関数 ---

def create_prompt_entry(category, label, prompt_content):
    prompts_data = load_prompts()
    categories = prompts_data.get('categories', {})

    if not category.strip():
        return "Error: カテゴリ名を入力してください。"
    if not label.strip():
        return "Error: ラベル名を入力してください。"

    if category not in categories:
        categories[category] = []

    for item in categories[category]:
        if item.get('label') == label:
            return "Error: このカテゴリにすでに同じラベルが存在します。"

    categories[category].append({'label': label, 'prompt': prompt_content})
    prompts_data['categories'] = categories
    save_prompts(prompts_data)
    return "プロンプト（ラベル）が正常に作成されました。"

def update_prompt_entry(old_category, old_label, new_category, new_label, new_prompt_content):
    prompts_data = load_prompts()
    categories = prompts_data.get('categories', {})

    if not new_category.strip():
        return "Error: 新しいカテゴリ名を入力してください。"
    if not new_label.strip():
        return "Error: 新しいラベル名を入力してください。"

    found_old = False
    if old_category in categories:
        original_category_list = categories[old_category]
        updated_category_list = [item for item in original_category_list if item.get('label') != old_label]
        if len(updated_category_list) < len(original_category_list):
            found_old = True
            categories[old_category] = updated_category_list
            if not categories[old_category]:
                del categories[old_category]

    if not found_old:
        return "Error: 更新対象の元のラベルが見つかりませんでした。カテゴリとラベルを正しく選択してください。"

    if new_category not in categories:
        categories[new_category] = []

    if (old_category != new_category) or (old_label != new_label):
        for item in categories[new_category]:
            if item.get('label') == new_label:
                if old_category == new_category and old_label == new_label:
                    pass
                else:
                    return "Error: ターゲットカテゴリに新しいラベルがすでに存在します。"

    categories[new_category].append({'label': new_label, 'prompt': new_prompt_content})
    prompts_data['categories'] = categories
    save_prompts(prompts_data)
    return "プロンプト（ラベル）が正常に更新されました。"

def delete_prompt_entry(category, label):
    prompts_data = load_prompts()
    categories = prompts_data.get('categories', {})

    if not category.strip() or not label.strip():
        return "Error: 削除するカテゴリとラベルを選択してください。"

    if category not in categories:
        return "Error: 削除対象のカテゴリが見つかりませんでした。"

    original_len = len(categories[category])
    categories[category] = [item for item in categories[category] if item.get('label') != label]

    if len(categories[category]) == original_len:
        return "Error: 削除対象のラベルが見つかりませんでした。"

    if not categories[category]:
        del categories[category]

    prompts_data['categories'] = categories
    save_prompts(prompts_data)
    return "プロンプト（ラベル）が正常に削除されました。"

# --- `scripts.Script` クラス ---

class Script(scripts.Script):
    def title(self):
        return "Prompt Manager"
        
    def show(self, is_img2img):
        return scripts.AlwaysVisible
    
    def ui(self, is_img2img):
        categories = get_categories()

        with gr.Accordion("Prompt Manager", open=False):
            gr.HTML(f"<style>{css}</style>")
            with gr.Tabs():
                # --- Manage Promptsタブ ---
                with gr.Tab("Manage Prompts"):
                    gr.Markdown("### プロンプトの管理")
                    with gr.Column():
                        with gr.Row():
                            existing_category_dropdown_manage = gr.Dropdown(
                                choices=categories,
                                label="カテゴリ",
                                interactive=True
                            )
                            existing_label_dropdown_manage = gr.Dropdown(
                                choices=[],
                                label="ラベル",
                                interactive=True
                            )
                            load_prompt_btn_manage = gr.Button("読み込み")
                        with gr.Column():
                            category_input_manage = gr.Textbox(label="カテゴリ名")
                            label_input_manage = gr.Textbox(label="ラベル名")
                            prompt_content_input_manage = gr.Textbox(
                                label="プロンプト内容",
                                lines=3
                            )
                            output_message_manage = gr.Markdown()
                        with gr.Row():
                            create_btn = gr.Button("新規作成", variant="primary")
                            update_btn = gr.Button("更新", variant="secondary")
                            delete_btn = gr.Button("削除", variant="stop")
                # --- Insert Promptsタブ ---
                with gr.Tab("Insert Prompts"):
                    gr.Markdown("### プロンプトを選択して挿入")
                    with gr.Column():
                        category_selector_insert = gr.Dropdown(
                            choices=categories,
                            label="カテゴリを選択",
                            interactive=True,
                            value=None
                        )
                        prompt_buttons_container = gr.HTML()

            # --- イベント接続 ---
            def create_prompt_buttons(selected_category):
                if not selected_category:
                    return ""
                labels = get_labels_by_category(selected_category)
                if not labels:
                    return "<p>このカテゴリにはラベルがありません。</p>"
                buttons_html = '<div style="display: flex; flex-wrap: wrap; gap: 8px;">'
                for label, content in labels.items():
                    escaped_content = html.escape(content)
                    escaped_label = html.escape(label)
                    buttons_html += f"""
                        <button
                            class="prompt-button"
                            onclick="(function(e) {{
                                // 通常クリックはプロンプト欄
                                let textarea = null;
                                const tabTxt2Img = gradioApp().querySelector('#tab_txt2img');
                                const tabImg2Img = gradioApp().querySelector('#tab_img2img');
                                if(tabTxt2Img && tabTxt2Img.style.display !== 'none') {{
                                    textarea = gradioApp().querySelector('#txt2img_prompt textarea');
                                }} else if(tabImg2Img && tabImg2Img.style.display !== 'none') {{
                                    textarea = gradioApp().querySelector('#img2img_prompt textarea');
                                }}
                                if(textarea) {{
                                    const content = '{escaped_content}';
                                    const start = textarea.selectionStart;
                                    const end = textarea.selectionEnd;
                                    const before = textarea.value.substring(0, start);
                                    const after = textarea.value.substring(end);
                                    const insert = (before && before.trim().length > 0 ? ', ' : '') + content;
                                    textarea.value = before + insert + after;
                                    // カーソルを挿入したテキストの後ろに移動
                                    const cursorPos = before.length + insert.length;
                                    textarea.setSelectionRange(cursorPos, cursorPos);
                                    textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                    textarea.focus();
                                }}
                            }})(event);"
                            oncontextmenu="(function(e) {{
                                e.preventDefault();
                                // 右クリックはネガティブプロンプト欄
                                let textarea = null;
                                const tabTxt2Img = gradioApp().querySelector('#tab_txt2img');
                                const tabImg2Img = gradioApp().querySelector('#tab_img2img');
                                if(tabTxt2Img && tabTxt2Img.style.display !== 'none') {{
                                    textarea = gradioApp().querySelector('#txt2img_neg_prompt textarea');
                                }} else if(tabImg2Img && tabImg2Img.style.display !== 'none') {{
                                    textarea = gradioApp().querySelector('#img2img_neg_prompt textarea');
                                }}
                                if(textarea) {{
                                    const content = '{escaped_content}';
                                    const start = textarea.selectionStart;
                                    const end = textarea.selectionEnd;
                                    const before = textarea.value.substring(0, start);
                                    const after = textarea.value.substring(end);
                                    const insert = (before && before.trim().length > 0 ? ', ' : '') + content;
                                    textarea.value = before + insert + after;
                                    // カーソルを挿入したテキストの後ろに移動
                                    const cursorPos = before.length + insert.length;
                                    textarea.setSelectionRange(cursorPos, cursorPos);
                                    textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                    textarea.focus();
                                }}
                            }})(event);"
                        >{escaped_label}</button>
                    """
                buttons_html += '</div>'
                return buttons_html

            category_selector_insert.change(
                fn=create_prompt_buttons,
                inputs=[category_selector_insert],
                outputs=prompt_buttons_container
            )

            load_prompt_btn_manage.click(
                fn=lambda c, l: (c, l, get_prompt_content(c, l)),
                inputs=[existing_category_dropdown_manage, existing_label_dropdown_manage],
                outputs=[category_input_manage, label_input_manage, prompt_content_input_manage]
            )

            existing_category_dropdown_manage.change(
                fn=lambda category: gr.Dropdown(choices=list(get_labels_by_category(category).keys()), value=None),
                inputs=existing_category_dropdown_manage,
                outputs=existing_label_dropdown_manage
            )

            create_btn.click(
                fn=create_prompt_entry,
                inputs=[category_input_manage, label_input_manage, prompt_content_input_manage],
                outputs=output_message_manage
            ).then(
                fn=lambda: (gr.Dropdown(choices=get_categories(), value=None), gr.Dropdown(choices=get_categories(), value=None)),
                outputs=[existing_category_dropdown_manage, category_selector_insert]
            ).then(
                fn=lambda: gr.Dropdown(choices=[], value=None),
                outputs=existing_label_dropdown_manage
            )

            update_btn.click(
                fn=update_prompt_entry,
                inputs=[existing_category_dropdown_manage, existing_label_dropdown_manage,
                        category_input_manage, label_input_manage, prompt_content_input_manage],
                outputs=output_message_manage
            ).then(
                fn=lambda: (gr.Dropdown(choices=get_categories(), value=None), gr.Dropdown(choices=get_categories(), value=None)),
                outputs=[existing_category_dropdown_manage, category_selector_insert]
            ).then(
                fn=lambda: gr.Dropdown(choices=[], value=None),
                outputs=existing_label_dropdown_manage
            )

            delete_btn.click(
                fn=delete_prompt_entry,
                inputs=[existing_category_dropdown_manage, existing_label_dropdown_manage],
                outputs=output_message_manage
            ).then(
                fn=lambda: (gr.Dropdown(choices=get_categories(), value=None), gr.Dropdown(choices=get_categories(), value=None)),
                outputs=[existing_category_dropdown_manage, category_selector_insert]
            ).then(
                fn=lambda: gr.Dropdown(choices=[], value=None),
                outputs=existing_label_dropdown_manage
            )

        return []

    def run(self, p, *args):
        return p