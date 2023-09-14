from st_pages import Page, add_page_title, show_pages

show_pages(
    [
        Page("st-pages/home.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        # The pages appear in the order you pass them
        Page("st-pages/presentation.py", "Presentation", "📽️"),
        Page("st-pages/schema.py", "Schema", "📝"),
        Page("st-pages/chatbot.py", "Text-to-SQL", "🤖️"),
        # Will use the default icon and name based on the filename if you don't
        # pass them
        # Page("pages/example_three.py"),
        # Page("pages/example_five.py", "Example Five", "🧰"),
    ]
)

# Optional method to add title and icon to current page
