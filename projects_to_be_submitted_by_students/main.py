import streamlit as st
import time
import random

# Store chat hist
st.set_page_config(page_title="Café Order Chatbot", page_icon="☕", layout="wide")

# Correct path to the header image
header_image = "cafe.png"  # Make sure the image file is in the same directory or provide full path
st.image(header_image, use_container_width=True)



# ory, orders, and user address
if "messages" not in st.session_state:
    st.session_state.messages = []
if "order" not in st.session_state:
    st.session_state.order = []
if "checkout" not in st.session_state:
    st.session_state.checkout = False
if "address" not in st.session_state:
    st.session_state.address = ""

# Menu items and prices (default values)
if "menu_items" not in st.session_state:
    st.session_state.menu_items = {
        "coffee": 5,
        "tea": 3,
        "sandwich": 7,
        "cake": 4
    }

# Possible delivery delays
delivery_reasons = ["heavy traffic", "bad weather", "high order volume", "technical issues"]

# Function to simulate bot response delay
def bot_reply(text):
    time.sleep(1)  # Simulate delay
    st.session_state.messages.append({"role": "bot", "text": text})

# Function to display chat messages
def display_chat():
    for msg in st.session_state.messages:
        if msg["role"] == "bot":
            with st.chat_message("assistant"):
                st.markdown(msg["text"], unsafe_allow_html=True)
        else:
            with st.chat_message("user"):
                st.markdown(msg["text"], unsafe_allow_html=True)

# Sidebar Authentication (for admin only)
admin_password = st.secrets["general"]["admin_password"]

# Add the password input in the sidebar
password = st.sidebar.text_input("Admin Password", type="password", key="admin_password")

# Check password and allow access to the admin menu
if password == admin_password:
    # Only show this sidebar to admins
    st.sidebar.header("Hotel Management")
    
    # Update Menu Items in the sidebar
    st.sidebar.subheader("Update Menu Items")
    item = st.sidebar.selectbox("Select item to update:", options=list(st.session_state.menu_items.keys()))
    new_price = st.sidebar.number_input(f"New Price for {item.capitalize()}", min_value=1, value=st.session_state.menu_items[item])

    if st.sidebar.button("Update Price"):
        st.session_state.menu_items[item] = new_price
        st.sidebar.success(f"{item.capitalize()} price updated to ${new_price}")
    
    # Add New Item to Menu
    st.sidebar.subheader("Add New Item to Menu")
    new_item = st.sidebar.text_input("New Item Name")
    new_item_price = st.sidebar.number_input("Price of New Item", min_value=1)
    
    if st.sidebar.button("Add New Item"):
        if new_item and new_item_price:
            st.session_state.menu_items[new_item.lower()] = new_item_price
            st.sidebar.success(f"New item '{new_item.capitalize()}' added with price ${new_item_price}")
        else:
            st.sidebar.warning("Please enter both item name and price.")
else:
    st.sidebar.markdown("**You are not authorized to access the admin section.**")

# Menu items and prices
menu_items = st.session_state.menu_items

# Function to display updated menu in chatbot
def show_updated_menu():
    menu_text = "**Here’s our menu:**\n"
    for item, price in menu_items.items():
        menu_text += f"- {item.capitalize()}: ${price}\n"
    bot_reply(menu_text)

# Streamlit App UI
st.title("☕ Café Order Chatbot")
st.write("Welcome to our café! How can I assist you today?")
st.markdown("""
    <style>
        .header {
            font-size: 32px;
            font-weight: bold;
            color: #FF6347; /* Tomato color */
            margin: 20px;
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
        }
            
        .stButton > button {
            background-color: #333333; /* Green */
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton > button:hover {
                background-color: #555555; /* Lighter gray on hover */
                text-decoration: underline;        }
        .stChatMessage {
            font-family: 'Arial', sans-serif;
            font-size: 14px;
        }
        .stChatMessage.assistant {
            background-color: #f0f0f0;
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
            max-width: 75%;
        }
        .stChatMessage.user {
            background-color: #007BFF; /* Blue */
            color: white;
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
            max-width: 75%;
        }
        .stChatMessage.assistant {
            align-self: flex-start;
        }
        .stChatMessage.user {
            align-self: flex-end;
        }
        .stTextInput input {
            font-size: 16px;
            padding: 10px;
            border-radius: 10px;
        }
        .stSidebar {
            background-color: #F0F0F0;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-family: 'Arial', sans-serif;
            font-size: 14px;
            color: #1A3D46;
        }
        .stSidebar .stTextInput input {
            font-size: 16px;
            padding: 10px;
            color: #1A3D46;
            padding: 20px;
            border-radius: 10px;
            padding: 20px;
        }
            
        .stApp {
            background-color: linear-gradient(to right, #FF6347, #FF7F50);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-family: 'Arial', sans-serif;
            font-size: 14px;
            color: #1A3D46;
        }
        .stApp .stTextInput input {
            font-size: 16px;
            padding: 10px;
            color: #1A3D46;
            padding: 20px;
            border-radius: 10px;
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)


# Display header
st.markdown('<div class="header">"Where Every Sip Feels Like Home!"</div>', unsafe_allow_html=True)
st.write("")
st.write("")
st.write("")


# Container for the chat


# Display chat history
display_chat()

# Predefined Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📜 View Menu", key="view_menu"):
        show_updated_menu()

with col2:
    if st.button("🛒 Place Order"):
        bot_reply("Sure! Please type the item you want to order.")

with col3:
    if st.button("📞 Talk to Team"):
        team_responses = [
            "Our team is looking into your request. Please hold on for a moment!",
            "Thank you for reaching out. We're checking on the issue. One moment, please.",
            "We're currently assisting other customers, but someone will be with you shortly.",
            "Sorry for the delay, our team is processing your request. Please bear with us!",
            "Our support team is gathering the details. We'll get back to you shortly!"
        ]
        bot_reply(random.choice(team_responses))
st.write("")

st.write("")

st.write("")


st.write("")

st.write("")
# User Input for Chat
user_input = st.chat_input("Type your message...")

# Process user input
if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input.lower()})
    
    words = user_input.lower().split()

    # Check if user wants to see the menu
    if "menu" in words:
        show_updated_menu()

    # Check if user is placing an order
    elif any(item in words for item in menu_items):
        ordered_items = [item for item in words if item in menu_items]
        st.session_state.order.extend(ordered_items)
        for item in ordered_items:
            bot_reply(f"Great choice! Your {item} has been added to your order.")

    # Check if user asks for total cost
    elif "total" in words or "bill" in words:
        if st.session_state.order:
            total = sum(menu_items[item] for item in st.session_state.order)
            bot_reply(f"Your total bill is **${total}**. Would you like to proceed to checkout?")
        else:
            bot_reply("You haven't ordered anything yet!")

    # Handle checkout process
    elif user_input.lower() in ["yes", "checkout", "proceed"]:
        if st.session_state.order:
            bot_reply("Great! Please share your delivery address.")
            st.session_state.checkout = True
        else:
            bot_reply("You need to add items before checking out!")

    # Capture delivery address
    elif st.session_state.checkout and st.session_state.address == "":
        st.session_state.address = user_input
        bot_reply(f"Thank you! Your order will be delivered to **{st.session_state.address}**.")

        # Estimate delivery time (random between 5-20 minutes)
        delivery_time = random.randint(5, 20)
        bot_reply(f"Your order will arrive in **{delivery_time} minutes**.")

        # Introduce a delay reason if delivery time is over 10 minutes
        if delivery_time > 10:
            reason = random.choice(delivery_reasons)
            bot_reply(f"🚨 Due to {reason}, your order might be slightly delayed. We apologize for the inconvenience.")

    # Check order status
    elif "status" in words or "track" in words:
        if st.session_state.order:
            bot_reply("Your order is being prepared! 🚀 It will arrive soon.")
        else:
            bot_reply("You haven't placed an order yet!")

    # Handle user complaints
    elif "bad experience" in user_input.lower() or "complaint" in user_input.lower():
        bot_reply("I'm really sorry to hear that! Please share more details, and we’ll work on improving.")

    # Handle unsupported queries
    else:
        bot_reply("I'm not sure how to answer that. Would you like to talk to our team? Type 'team' to connect with support.")

# Refresh chat after user input
display_chat()

st.markdown('</div>', unsafe_allow_html=True)
