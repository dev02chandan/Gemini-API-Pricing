import streamlit as st

def calculate_cost(model, api_calls_per_day, avg_input_length, avg_output_length, video_seconds_per_day, audio_seconds_per_day, context_window):
    if model == 'Gemini 1.5 Flash':
        if context_window == '<= 128K':
            image_cost = 0.0001315 * api_calls_per_day
            video_cost = 0.0001315 * video_seconds_per_day
            text_input_cost = 0.000125 * (api_calls_per_day * avg_input_length / 1000)
            audio_cost = 0.000125 * audio_seconds_per_day
            text_output_cost = 0.000375 * (api_calls_per_day * avg_output_length / 1000)
        else:
            image_cost = 0.000263 * api_calls_per_day
            video_cost = 0.000263 * video_seconds_per_day
            text_input_cost = 0.00025 * (api_calls_per_day * avg_input_length / 1000)
            audio_cost = 0.00025 * audio_seconds_per_day
            text_output_cost = 0.00075 * (api_calls_per_day * avg_output_length / 1000)
    elif model == 'Gemini 1.5 Pro':
        if context_window == '<= 128K':
            image_cost = 0.001315 * api_calls_per_day
            video_cost = 0.001315 * video_seconds_per_day
            text_input_cost = 0.00125 * (api_calls_per_day * avg_input_length / 1000)
            audio_cost = 0.000125 * audio_seconds_per_day
            text_output_cost = 0.00375 * (api_calls_per_day * avg_output_length / 1000)
        else:
            image_cost = 0.00263 * api_calls_per_day
            video_cost = 0.00263 * video_seconds_per_day
            text_input_cost = 0.0025 * (api_calls_per_day * avg_input_length / 1000)
            audio_cost = 0.00025 * audio_seconds_per_day
            text_output_cost = 0.0075 * (api_calls_per_day * avg_output_length / 1000)
    elif model == 'Gemini 1.0 Pro':
        image_cost = 0.0025 * api_calls_per_day
        video_cost = 0.002 * video_seconds_per_day
        text_input_cost = 0.000125 * (api_calls_per_day * avg_input_length / 1000)
        text_output_cost = 0.000375 * (api_calls_per_day * avg_output_length / 1000)
        audio_cost = 0
    
    daily_total_cost = image_cost + video_cost + text_input_cost + audio_cost + text_output_cost
    monthly_total_cost = daily_total_cost * 30
    return daily_total_cost, monthly_total_cost, image_cost, video_cost, text_input_cost, audio_cost, text_output_cost

st.title("Gemini API Cost Comparison")

st.sidebar.header("Daily Usage Inputs")
api_calls_per_day = st.sidebar.number_input("Average number of API calls per day", min_value=0, value=100)
avg_input_length = st.sidebar.number_input("Average input sequence length", min_value=0, value=100)
avg_output_length = st.sidebar.number_input("Average output sequence length", min_value=0, value=100)
video_seconds_per_day = st.sidebar.number_input("Total duration of videos processed per day (in seconds)", min_value=0, value=100)
audio_seconds_per_day = st.sidebar.number_input("Total duration of audio processed per day (in seconds)", min_value=0, value=100)
context_window = st.sidebar.selectbox("Context Window", ["<= 128K", "> 128K"], index=0)

st.sidebar.header("Model Selection")
model = st.sidebar.selectbox("Select the Model", ["Gemini 1.5 Flash", "Gemini 1.5 Pro", "Gemini 1.0 Pro"])

if st.sidebar.button("Calculate Cost"):
    daily_total_cost, monthly_total_cost, image_cost, video_cost, text_input_cost, audio_cost, text_output_cost = calculate_cost(
        model, api_calls_per_day, avg_input_length, avg_output_length, video_seconds_per_day, audio_seconds_per_day, context_window)
    
    st.write(f"## Total Daily Cost for {model}: ${daily_total_cost:.2f}")
    st.write(f"## Total Monthly Cost for {model}: ${monthly_total_cost:.2f}")
    
    st.write("### Detailed Costs Breakdown")
    
    st.write(f"**1. Image Input Cost**")
    st.write(f"- Number of API calls per day: {api_calls_per_day}")
    st.write(f"- Number of API calls per month: {api_calls_per_day * 30}")
    st.write(f"- Cost per image: ${image_cost / api_calls_per_day:.6f}")
    st.write(f"- Daily image input cost: ${image_cost:.2f}")
    st.write(f"- Monthly image input cost: ${image_cost * 30:.2f}")

    st.write(f"**2. Video Input Cost**")
    st.write(f"- Total duration of videos processed per day: {video_seconds_per_day} seconds")
    st.write(f"- Total duration of videos processed per month: {video_seconds_per_day * 30} seconds")
    st.write(f"- Cost per second of video: ${video_cost / video_seconds_per_day:.6f}")
    st.write(f"- Daily video input cost: ${video_cost:.2f}")
    st.write(f"- Monthly video input cost: ${video_cost * 30:.2f}")

    st.write(f"**3. Text Input Cost**")
    st.write(f"- Total number of characters processed per day: {api_calls_per_day * avg_input_length}")
    st.write(f"- Total number of characters processed per month: {api_calls_per_day * avg_input_length * 30}")
    st.write(f"- Cost per 1k characters: ${text_input_cost / (api_calls_per_day * avg_input_length / 1000):.6f}")
    st.write(f"- Daily text input cost: ${text_input_cost:.2f}")
    st.write(f"- Monthly text input cost: ${text_input_cost * 30:.2f}")

    st.write(f"**4. Audio Input Cost**")
    st.write(f"- Total duration of audio processed per day: {audio_seconds_per_day} seconds")
    st.write(f"- Total duration of audio processed per month: {audio_seconds_per_day * 30} seconds")
    st.write(f"- Cost per second of audio: ${audio_cost / audio_seconds_per_day:.6f}")
    st.write(f"- Daily audio input cost: ${audio_cost:.2f}")
    st.write(f"- Monthly audio input cost: ${audio_cost * 30:.2f}")

    st.write(f"**5. Text Output Cost**")
    st.write(f"- Total number of characters generated per day: {api_calls_per_day * avg_output_length}")
    st.write(f"- Total number of characters generated per month: {api_calls_per_day * avg_output_length * 30}")
    st.write(f"- Cost per 1k characters: ${text_output_cost / (api_calls_per_day * avg_output_length / 1000):.6f}")
    st.write(f"- Daily text output cost: ${text_output_cost:.2f}")
    st.write(f"- Monthly text output cost: ${text_output_cost * 30:.2f}")
    # Summary

    st.write("### Summary")
    st.write(f"- **Monthly image input cost**: ${image_cost * 30:.2f}")
    st.write(f"- **Monthly video input cost**: ${video_cost * 30:.2f}")
    st.write(f"- **Monthly text input cost**: ${text_input_cost * 30:.2f}")
    st.write(f"- **Monthly audio input cost**: ${audio_cost * 30:.2f}")
    st.write(f"- **Monthly text output cost**: ${text_output_cost * 30:.2f}")
    st.write(f"- **Total monthly cost**: ${monthly_total_cost:.2f}")

    st.write("""
    Check the [Gemini API Pricing Page](https://cloud.google.com/vertex-ai/generative-ai/pricing#:~:text=Price-,Gemini%20Pro,-Multimodal).
    """)
