root@eeifqjcblj:~# grep -n "chat\|Chat\|console\|Console" /root/paradust-wasm/sources/minetest/src/gui/touchcontrols.cpp | head -30
188:            case toggle_chat_id:
189:                    key = "toggle_chat";
191:            case chat_id:
192:                    key = "chat";
314:            if (id == toggle_chat_id)
315:                    // Chat is shown by default, so chat_hide_btn.png is shown first.
316:                    addToggleButton(m_buttons, id, "chat_hide_btn.png",
317:                                    "chat_show_btn.png", rect, true);
342:            if (id == toggle_chat_id)
343:                    // Chat is shown by default, so chat_hide_btn.png is shown first.
344:                    addToggleButton(m_overflow_buttons, id, "chat_hide_btn.png",
345:                                    "chat_show_btn.png", rect, false);
root@eeifqjcblj:~#
