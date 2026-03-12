
### Pseudo-code Breakdown (Very Rough)

```pseudo
// 1. Page loads
ON PAGE LOAD:
    show bot message: "Hello! How can I help..."
    focus on input box (so mobile users can type instantly)

// 2. User sends message (two ways)
WHEN user presses Enter OR clicks Send button:
    get text from input box
    if text is empty → do nothing
    else:
        add user message bubble (blue, right side)
        clear input box
        call getResponse(text) → get bot reply
        wait 400ms (fake thinking 😴)
        add bot message bubble (light blue, left side)
        scroll chat to bottom

WHEN user clicks any Quick Button (Timings, Fees, etc.):
    pretend user typed that question
    add it as user message
    instantly get bot reply
    show both bubbles
    focus back to input box

// 3. The "Brain" – getResponse function (keyword matching)
FUNCTION getResponse(userQuestion):
    lowercase everything & trim spaces

    IF question contains "hi" OR "hello" OR "hey":
        RETURN greeting message

    ELSE IF contains "time" OR "hours" OR "open" OR "schedule":
        RETURN "Monday to Friday, 9 AM to 5 PM"

    ELSE IF contains "fee" OR "cost" OR "price" OR "tuition":
        RETURN fee info

    ELSE IF contains "contact" OR "phone" OR "call" OR "address":
        RETURN "0712 619 2403 | 123 Education Lane"

    ELSE IF contains "apply" OR "admission":
        RETURN admission info

    ELSE IF contains "course" OR "program":
        RETURN list of courses

    ELSE IF contains "scholarship":
        RETURN scholarship details

    ELSE IF contains "job" OR "placement":
        RETURN placement info

    ELSE IF contains "hostel" OR "housing":
        RETURN hostel info

    ELSE IF contains "teacher" OR "faculty":
        RETURN faculty info

    ELSE:
        RETURN sorry message + suggest common topics

// 4. Adding messages to screen
FUNCTION addMessage(text, type):  // type = "user" or "bot"
    create new <div class="message type">
    put text inside
    add to chat-container
    scroll to bottom (so newest message visible)
