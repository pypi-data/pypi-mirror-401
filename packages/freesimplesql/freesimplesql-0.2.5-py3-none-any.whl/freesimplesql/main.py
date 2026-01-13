import FreeSimpleGUI as sg
from sqlalchemy.sql import text

from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime, timedelta
import random
import ipaddress
import json
from typing import Optional
from faker import Faker
from loguru import logger
from pydantic import field_validator
import shutil
import requests
import os

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sn: int
    timestamp: datetime
    src_ip: str
    dst_ip: str
    msg_name: str
    msg_content: str
    hexvalue: str

    @field_validator("timestamp", mode="before")
    def validate_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

class DBBrowser:
    def __init__(self):
        self.engine = create_engine("sqlite:///database.db", echo=False)
        self.page_size = 50 * 10
        self.default_query = "SELECT * FROM message"
        self.current_page = 0
        self.total_rows = 0

    @staticmethod
    def setup_db():
        SQLModel.metadata.create_all(DBBrowser.create_engine())
        with Session(DBrowser.create_engine()) as session:
            if not session.exec(select(Message)).first():
                DBrowser.generate_dummy_data()

    @staticmethod
    def create_engine():
        return create_engine("sqlite:///database.db", echo=False)

    @staticmethod
    def generate_dummy_data():
        fake = Faker()
        msg_names = ["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"]
        base_time = datetime.now()
        with Session(DBrowser.create_engine()) as session:
            messages = []
            for i in range(1000):
                json_content = {
                    "id": i + 1,
                    "name": fake.name(),
                    "email": fake.email(),
                    "address": fake.address(),
                    "text": fake.text(max_nb_chars=900)
                }
                json_str = json.dumps(json_content)
                hex_value = json_str.encode("utf-8").hex()
                message = Message(
                    sn=i + 1,
                    timestamp=base_time + timedelta(seconds=i),
                    src_ip=str(ipaddress.IPv4Address(random.randint(0, 2**32-1))),
                    dst_ip=str(ipaddress.IPv4Address(random.randint(0, 2**32-1))),
                    msg_name=random.choice(msg_names),
                    msg_content=json_str,
                    hexvalue=hex_value
                )
                messages.append(message)
            session.add_all(messages)
            session.commit()

    def execute_query(self, query_text=None):
        with Session(self.engine) as session:
            try:
                # Calculate LIMIT and OFFSET for pagination
                limit = self.page_size
                offset = self.current_page * self.page_size
                paginated_query = None
                if query_text and query_text.strip():
                    # Remove any existing LIMIT/OFFSET from user query for safety
                    base_query = query_text.strip().rstrip(';')
                    if 'limit' in base_query.lower():
                        base_query = base_query.rsplit('limit', 1)[0].strip()
                    paginated_query = f"{base_query} LIMIT {limit} OFFSET {offset}"
                    logger.debug(f"Executing paginated SQL query: {paginated_query}")
                    result = session.exec(text(paginated_query))
                    all_results = [Message(**dict(zip(result.keys(), row))) for row in result]
                    # Get total rows for pagination info
                    count_query = f"SELECT COUNT(*) FROM ({base_query}) as subquery"
                    total = session.exec(text(count_query)).first()
                    self.total_rows = total[0] if total else 0
                else:
                    logger.debug("Executing default paginated query using SQLModel")
                    result = session.exec(select(Message).offset(offset).limit(limit))
                    all_results = list(result)
                    # Get total rows for pagination info
                    self.total_rows = session.exec(select(Message)).count()
                logger.debug(f"Query returned {len(all_results)} rows (page {self.current_page + 1})")
                return all_results
            except Exception as e:
                logger.debug(f"Query error: {e}")
                self.total_rows = 0
                return []

    def update_record(self, record_id: int, new_data: dict):
        with Session(self.engine) as session:
            try:
                record = session.get(Message, record_id)
                if not record:
                    return False, "Record not found"
                
                # Update fields
                for key, value in new_data.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                
                session.add(record)
                session.commit()
                session.refresh(record)
                return True, "Success"
            except Exception as e:
                logger.error(f"Update failed: {e}")
                return False, str(e)

                return False, str(e)

    def get_schema(self):
        try:
            with Session(self.engine) as session:
                # specific for sqlite
                result = session.exec(text("SELECT sql FROM sqlite_master WHERE type='table' AND name='message'")).first()
                if result:
                    return result[0]
                return "Schema not found."
        except Exception as e:
            return f"Error retrieving schema: {e}"

    def get_columns(self):
        return ["sn", "timestamp", "src_ip", "dst_ip", "msg_name", "msg_content", "hexvalue"]

    def get_row_dict(self, row: Message):
        return {
            "sn": row.sn,
            "timestamp": row.timestamp,
            "src_ip": row.src_ip,
            "dst_ip": row.dst_ip,
            "msg_name": row.msg_name,
            "msg_content": row.msg_content,
            "hexvalue": row.hexvalue
        }




# --- Settings Persistence ---
SETTINGS_FILE = 'settings.json'
STATE_FILE = 'app_state.json'

def load_settings():
    default_settings = {
        'url': 'https://openrouter.ai/api/v1/chat/completions',
        'model': 'google/gemini-2.0-flash-exp:free',
        'key': '',
        'theme': 'SystemDefaultForReal'
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return {**default_settings, **json.load(f)}
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
    return default_settings

def save_settings(url, model, key, theme=None):
    try:
        data = {'url': url, 'model': model, 'key': key}
        if theme:
            data['theme'] = theme
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"Failed to save settings: {e}")

def load_state():
    """Load UI state (query, prompt, history) from disk"""
    default_state = {
        'query': 'SELECT * FROM message',
        'prompt': '',
        'history': ''
    }
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return {**default_state, **json.load(f)}
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
    return default_state

def save_state(query, prompt, history):
    """Save UI state (query, prompt, history) to disk"""
    try:
        data = {
            'query': query,
            'prompt': prompt,
            'history': history
        }
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save state: {e}")

def main():
    settings = load_settings()
    state = load_state()  # Load saved UI state
    sg.theme(settings.get('theme', 'SystemDefaultForReal'))
    
    browser = DBBrowser()
    settings = load_settings()

    # Get all column names from SQLModel
    columns = list(Message.model_fields.keys())

    current_page_rows = []  # Store the current page's row objects

    def update_table(query_text=None):
        nonlocal current_page_rows
        # logger.debug("Updating table with new query results")
        rows = browser.execute_query(query_text)
        table_data = [[getattr(row, col) for col in columns] for row in rows]
        window['-TABLE-'].update(values=table_data)
        current_page_rows = rows  
        max_pages = (browser.total_rows - 1) // browser.page_size + 1 if browser.total_rows > 0 else 1
        window['-PAGE_INFO-'].update(f"Page {browser.current_page + 1} of {max_pages}")

    def open_edit_modal(row_data: Message):
        """Opens a modal to edit the selected record."""
        layout = []
        fields = ["sn", "timestamp", "src_ip", "dst_ip", "msg_name", "msg_content", "hexvalue"]
        
        for field in fields:
            val = getattr(row_data, field)
            if field in ['msg_content', 'hexvalue']:
                # Format JSON content for better readability
                display_val = val
                if field == 'msg_content':
                    try:
                        # Try to parse and pretty-print JSON
                        parsed = json.loads(val)
                        display_val = json.dumps(parsed, indent=2, ensure_ascii=False)
                    except (json.JSONDecodeError, TypeError):
                        # If not valid JSON, display as-is
                        display_val = val
                layout.append([sg.Text(field, size=(15, 1)), sg.Multiline(display_val, key=field, size=(50, 8), expand_x=True, expand_y=True)])
            else:
                layout.append([sg.Text(field, size=(15, 1)), sg.Input(val, key=field, expand_x=True)])
            
        layout.append([sg.Button('Save'), sg.Button('Cancel')])
        
        edit_window = sg.Window('Edit Record', layout, modal=True, finalize=True, resizable=True, size=(1000, 800))
        
        ret_val = None
        while True:
            e, v = edit_window.read()
            if e in (sg.WIN_CLOSED, 'Cancel'):
                break
            if e == 'Save':
                try:
                    cleaned_data = v.copy()
                    cleaned_data['sn'] = int(v['sn'])
                    ts_val = v['timestamp']
                    if isinstance(ts_val, str):
                        if ' ' in ts_val and 'T' not in ts_val:
                            ts_val = ts_val.replace(' ', 'T')
                        cleaned_data['timestamp'] = datetime.fromisoformat(ts_val)
                    
                    try:
                        ipaddress.ip_address(cleaned_data['src_ip'])
                        ipaddress.ip_address(cleaned_data['dst_ip'])
                    except ValueError:
                        raise ValueError("Invalid IP Address format")
                        
                    try:
                        # Validate and normalize JSON (remove formatting)
                        parsed_content = json.loads(cleaned_data['msg_content'])
                        cleaned_data['msg_content'] = json.dumps(parsed_content, ensure_ascii=False)
                    except json.JSONDecodeError:
                          raise ValueError("Invalid JSON in msg_content")
                          
                    ret_val = cleaned_data
                    break
                except ValueError as ve:
                    sg.popup_error(f"Validation Error: {ve}")
                except Exception as e:
                    sg.popup_error(f"Error: {e}")

        edit_window.close()
        return ret_val

    # --- Layout columns ---
    
    # 1. AI Configuration & Prompt (Replaces top section)
    ai_config_layout = [
        [sg.Text('URL:', size=(5, 1)), sg.Input(settings['url'], key='-AI-URL-', expand_x=True),
         sg.Text('Model:', size=(5, 1)), sg.Input(settings['model'], key='-AI-MODEL-', expand_x=True)],
        [sg.Text('Key:', size=(5, 1)), sg.Input(settings['key'], key='-AI-KEY-', password_char='*', expand_x=True)]
    ]
    
    ai_prompt_layout = [
        [sg.Text("Natural Language Prompt:"), sg.Push()],
        [sg.Multiline(default_text=state['prompt'], size=(60, 3), key='-AI-PROMPT-', expand_x=True, enter_submits=True)],
        [sg.Button('Generate SQL', key='-AI-GENERATE-')]
    ]

    # Get available themes
    available_themes = sg.theme_list()
    current_theme = sg.theme()
    
    # Action Buttons
    action_buttons_row = [
        sg.Button('Search', key='-SEARCH-'),
        sg.Button('Reset', key='-RESET-'),
        sg.Push(),
        sg.Text('Theme:', size=(5, 1)),
        sg.Combo(available_themes, default_value=current_theme, key='-THEME-', size=(20, 1), enable_events=True, readonly=True),
        sg.Button('Export DB', key='-EXPORT-'),
        sg.Button('Import DB', key='-IMPORT-')
    ]

    # --- LEFT PANE CONTENT ---
    left_pane_content = [
        [sg.Frame('AI Builder Settings', ai_config_layout, expand_x=True)],
        *ai_prompt_layout,
        [sg.Text("SQL Query (Generated/Editable):")],
        # This Multiline replaces the old -QUERY- and -AI-RESPONSE-
        [sg.Multiline(default_text=state['query'], size=(60, 6), key='-QUERY-', expand_x=True, expand_y=True)],
        action_buttons_row,
        [sg.HorizontalSeparator()],
        [sg.Text("Data Table:")],
        [sg.Table(
            values=[],
            headings=columns,
            auto_size_columns=True,
            display_row_numbers=False,
            justification='left',
            num_rows=20,
            key='-TABLE-',
            enable_events=True,
            expand_x=True,
            expand_y=True
        )],
        [
            sg.Button('First', key='-FIRST-'),
            sg.Button('Previous', key='-PREVIOUS-'),
            sg.Text('', key='-PAGE_INFO-', size=(20, 1), justification='center'),
            sg.Button('Next', key='-NEXT-'),
            sg.Button('Last', key='-LAST-')
        ]
    ]

    # --- RIGHT PANE CONTENT (History + Details + Schema Context) ---
    # Moved Schema here as a tab or just context? User said "condition builder shall includes all db fields"
    # User didn't ask to remove Context, but AI Builder Tab is gone. I'll put Schema in a Tab in Right Pane.
    right_pane_content = [
        [sg.Text("Query History:")],
        [sg.Multiline(default_text=state['history'], size=(30, 10), key='-HISTORY-', disabled=True, expand_x=True, expand_y=True)],
        [sg.HorizontalSeparator()],
        [sg.TabGroup([
            [
                sg.Tab('Detail View', [[sg.Multiline(size=(40, 30), key='-DETAIL-', disabled=True, expand_x=True, expand_y=True)]], key='-DETAIL-TAB-'),
                sg.Tab('Compact View', [[sg.Multiline(size=(40, 30), key='-COMPACT-', disabled=True, expand_x=True, expand_y=True)]], key='-COMPACT-TAB-'),
                sg.Tab('Schema Context', [[sg.Multiline(size=(40, 30), key='-SCHEMA-CONTEXT-', disabled=True, expand_x=True, expand_y=True)]], key='-SCHEMA-TAB-')
            ]
        ], key='-TABS-', expand_x=True, expand_y=True)]
    ]

    # Use sg.Column to wrap contents for Pane
    left_col = sg.Column(left_pane_content, expand_x=True, expand_y=True, key='-LEFT-PANE-', size=(1080, 800))
    right_col = sg.Column(right_pane_content, expand_x=True, expand_y=True, key='-RIGHT-PANE-', size=(720, 800))

    layout = [
        [sg.Pane([left_col, right_col], orientation='horizontal', relief=sg.RELIEF_GROOVE, expand_x=True, expand_y=True, show_handle=True)]
    ]

    window = sg.Window('FreeSimpleSQL', layout, resizable=True, finalize=True, size=(1800, 900))
    
    # Initialize Schema Text in the new tab
    window['-SCHEMA-CONTEXT-'].update(browser.get_schema())
    
    # Use LIMIT for the default query
    update_table(browser.default_query)
        
    # Bind double click event
    window['-TABLE-'].bind('<Double-Button-1>', '+DOUBLE_CLICK+')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            # Save state before closing
            save_state(
                values['-QUERY-'],
                values['-AI-PROMPT-'],
                values['-HISTORY-']
            )
            break
        elif event == '-THEME-':
            # Change theme immediately by saving and restarting
            new_theme = values['-THEME-']
            # Save all current settings including the new theme
            save_settings(
                values['-AI-URL-'],
                values['-AI-MODEL-'],
                values['-AI-KEY-'],
                new_theme
            )
            # Save current UI state before restart
            save_state(
                values['-QUERY-'],
                values['-AI-PROMPT-'],
                values['-HISTORY-']
            )
            # Close current window and restart with new theme
            window.close()
            main()
            return
        elif event == '-AI-GENERATE-':
            url = values['-AI-URL-'].strip()
            model = values['-AI-MODEL-'].strip()
            api_key = values['-AI-KEY-'].strip()
            prompt = values['-AI-PROMPT-'].strip()
            # Get schema from the hidden/right pane tab
            schema = values['-SCHEMA-CONTEXT-'] 
            
            # Save settings
            save_settings(url, model, api_key)

            if not api_key:
                sg.popup_error("Please enter an API Key.")
                continue
            
            if not prompt:
                sg.popup_error("Please enter a natural language prompt.")
                continue

            # Validate URL
            if not url.startswith('http'):
                sg.popup_error("Invalid API URL. Must start with http:// or https://")
                continue

            full_prompt = f"Given the following SQLite schema:\n{schema}\n\nWrite a SQL query for: {prompt}\nOnly return the SQL, no markdown or explanation."
            
            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ]
            }
            
            # Match OpenRouter's exact example format
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            try:
                window.set_cursor('wait')
                
                # Make the API request using the exact format from OpenRouter's example
                response = requests.post(
                    url=url,
                    headers=headers,
                    data=json.dumps(payload),  # Using data=json.dumps() as in their example
                    timeout=60
                )
                
                # Log the response for debugging
                logger.debug(f"API Response Status: {response.status_code}")
                logger.debug(f"API Response Headers: {response.headers}")
                
                if response.status_code == 200:
                    data = response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        content = data['choices'][0]['message']['content']
                        # Clean up markdown formatting
                        content = content.replace('```sql', '').replace('```', '').strip()
                        # Update the Main Query Window
                        window['-QUERY-'].update(content)
                        # Save state to preserve the generated query
                        save_state(content, values['-AI-PROMPT-'], values['-HISTORY-'])
                        sg.popup_quick_message('SQL generated successfully!', background_color='green', text_color='white')
                    else:
                        sg.popup_error(f"No content in response.\n\nResponse: {data}")
                elif response.status_code == 401:
                    error_detail = response.text
                    sg.popup_error(
                        f"Authentication Error (401)\n\n"
                        f"Your API key may be invalid or expired.\n\n"
                        f"Server response: {error_detail}\n\n"
                        f"Tips:\n"
                        f"1. Verify your API key is correct\n"
                        f"2. Check if your key has the required permissions\n"
                        f"3. Ensure you're using the correct API endpoint\n"
                        f"4. For OpenRouter, keys should start with 'sk-or-...'\n"
                        f"5. Get a key at: https://openrouter.ai/keys"
                    )
                else:
                    sg.popup_error(f"Error {response.status_code}\n\n{response.text}")

            except requests.exceptions.Timeout:
                sg.popup_error("Request timed out. The API server may be slow or unavailable.")
            except requests.exceptions.ConnectionError:
                sg.popup_error(f"Connection error. Could not reach: {url}")
            except requests.exceptions.RequestException as e:
                sg.popup_error(f"Request Error: {str(e)}")
            except Exception as e:
                sg.popup_error(f"Unexpected Error: {str(e)}")
            finally:
                window.set_cursor('arrow')

        elif event == '-TABLE-+DOUBLE_CLICK+':
            if len(values['-TABLE-']) > 0:
                row_idx = values['-TABLE-'][0]
                # Check if row_idx is valid
                if row_idx < len(current_page_rows):
                    row_data = current_page_rows[row_idx]
                    new_values = open_edit_modal(row_data)
                    if new_values:
                        success, pid = browser.update_record(row_data.id, new_values)
                        if success:
                            # Refresh table
                            update_table(values['-QUERY-'].strip())
                        else:
                            sg.popup_error(f"Failed to update record: {pid}")
                            
        elif event == '-EXPORT-':
            export_path = sg.popup_get_file('Save database as...', save_as=True, default_extension='.db', file_types=(('SQLite DB', '*.db'),))
            if export_path:
                
                try:
                    shutil.copy('database.db', export_path)
                    logger.debug(f"Database exported to {export_path}")
                    sg.popup('Database exported successfully!', title='Export')
                except Exception as e:
                    sg.popup(f'Export failed: {e}', title='Export Error')
                    logger.debug(f"Export failed: {e}")
                    
        elif event == '-IMPORT-':
            import_path = sg.popup_get_file(
                'Select SQLite database to import',
                file_types=(('SQLite DB', '*.db;*.sqlite;*.sqlite3'),)
            )
            if import_path:
                try:
                    logger.debug(f"Importing database from {import_path}")
                    sg.popup('Database imported successfully! Restarting view...', title='Import')

                    browser.engine = create_engine(f'sqlite:///{import_path}', echo=False)
                    browser.current_page = 0
                    update_table(browser.default_query)
                except Exception as e:
                    sg.popup(f'Import failed: {e}', title='Import Error')
        elif event == '-RESET-':
            browser.current_page = 0
            window['-QUERY-'].update(browser.default_query)  # Reset textarea to default query
            update_table(browser.default_query)
        elif event == '-SEARCH-':
            browser.current_page = 0
            query = values['-QUERY-'].strip()
            if query:
                # Build history entry with prompt and SQL
                prompt = values['-AI-PROMPT-'].strip()
                history_entry = ""
                if prompt:
                    history_entry += f"Prompt: {prompt}\n"
                history_entry += f"SQL: {query}\n--------\n"
                
                # Add to the top of the history
                history = window['-HISTORY-'].get()
                updated_history = f"{history_entry}{history}" if history else history_entry
                window['-HISTORY-'].update(updated_history)
                # Save state to preserve history
                save_state(query, prompt, updated_history)
                update_table(query)
        
        # --- Operator Buttons: Just append text ---
        elif event == '-NOT-FILTER-':
            current_query = values['-QUERY-'].strip()
            updated_query = f"{current_query} NOT "
            window['-QUERY-'].update(updated_query)                
        elif event == '-ADD-FILTER-':
            current_query = values['-QUERY-'].strip()
            updated_query = f"{current_query} AND "
            window['-QUERY-'].update(updated_query)
        elif event == '-OR-FILTER-':
            current_query = values['-QUERY-'].strip()
            updated_query = f"{current_query} OR "
            window['-QUERY-'].update(updated_query)
        elif event == '-OPEN-BRACKET-':
            current_query = values['-QUERY-'].strip()
            updated_query = f"{current_query} ( "
            window['-QUERY-'].update(updated_query)
        elif event == '-CLOSE-BRACKET-':
            current_query = values['-QUERY-'].strip()
            updated_query = f"{current_query} ) "
            window['-QUERY-'].update(updated_query)
            
        elif event == '-SHOW-SCHEMA-':
            # Open the new AI Builder
            open_ai_builder(browser.get_schema())

        # Check for Append Condition buttons (0-3)
        if isinstance(event, str) and event.startswith('-APPEND-CONDITION-'):
            try:
                # event format: -APPEND-CONDITION-0-
                idx = int(event.split('-')[3])
                col = values[f'-FILTER-COL-{idx}-']
                op = values[f'-FILTER-OP-{idx}-']
                val = values[f'-FILTER-VALUE-{idx}-']
                if col and op and val:
                    condition = f"{col} {op} '{val}'"
                    current_query = values['-QUERY-'].strip()
                    updated_query = f"{current_query} {condition}"
                    window['-QUERY-'].update(updated_query)
            except Exception as e:
                logger.error(f"Error appending condition: {e}")
                
        elif event == '-FIRST-':
            browser.current_page = 0
            update_table(values['-QUERY-'].strip())
        elif event == '-PREVIOUS-':
            if browser.current_page > 0:
                browser.current_page -= 1
                update_table(values['-QUERY-'].strip())
        elif event == '-NEXT-':
            if (browser.current_page + 1) * browser.page_size < browser.total_rows:
                browser.current_page += 1
                update_table(values['-QUERY-'].strip())
        elif event == '-LAST-':
            browser.current_page = (browser.total_rows - 1) // browser.page_size
            update_table(values['-QUERY-'].strip())
        elif event == '-TABLE-':
            if values['-TABLE-']:
                selected_idx = values['-TABLE-'][0]
                # Use the cached rows for the current page
                rows = current_page_rows
                if selected_idx < len(rows):
                    row = rows[selected_idx]
                    row_dict = browser.get_row_dict(row)
                    if 'msg_content' in row_dict:
                        try:
                            parsed_content = json.loads(row_dict['msg_content'])
                            row_dict['msg_content'] = parsed_content
                        except json.JSONDecodeError:
                            logger.debug("Failed to parse `msg_content` as JSON.")
                    pretty_json = json.dumps(row_dict, indent=4, default=str)
                    window['-DETAIL-'].update(pretty_json)
                    window['-COMPACT-'].update("\n".join([f"{k}: {v}" for k, v in row_dict.items()]))
                else:
                    logger.debug("Selected index is out of range for the query result.")

    window.close()

if __name__ == "__main__":
    main()

