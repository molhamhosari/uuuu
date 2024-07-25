from flask import Flask, request, jsonify
import openai
import logging

app = Flask(__name__)

# إعداد مفتاح API الخاص بـ OpenAI مباشرة في الشيفرة
openai.api_key = "sk-proj-3vl35MNtFHo3XYS2aeRRT3BlbkFJaXO5czgDbrMKRa45MMit"

# إعداد التسجيل (logging)
logging.basicConfig(level=logging.DEBUG)

# قاموس للأسئلة والأجوبة من النص المقدم باللغة الإنجليزية
faq = {
    "What is financial analysis?": "Financial analysis is the process of evaluating the financial activities of a company using financial data.",
    "What are the tools of financial analysis?": "Financial analysis tools include financial ratios, horizontal and vertical analysis, and cash flow analysis.",
    "What is the current ratio?": "The current ratio is the ratio of current assets to current liabilities, used to evaluate a company's ability to pay short-term debts.",
    "What is the quick ratio?": "The quick ratio is the ratio of quick assets (cash, marketable securities, and receivables) to current liabilities.",
    "What is the cash ratio?": "The cash ratio is the ratio of cash and marketable securities to current liabilities.",
    "What is the turnover ratio?": "The turnover ratio is the ratio of current assets to current liabilities.",
    "What is horizontal analysis?": "Horizontal analysis involves comparing financial data over different periods to identify trends and changes.",
    "What is vertical analysis?": "Vertical analysis involves analyzing financial statement items as a percentage of a base item such as sales or total assets.",
    "What is profitability ratio?": "Profitability ratios measure a company's ability to generate profit relative to its revenue, assets, or equity.",
    "What is debt ratio?": "Debt ratio measures the amount of debt a company has compared to its total capital.",
    "What is equity ratio?": "Equity ratio is the ratio of shareholders' equity to total assets.",
    "What is operating cash flow?": "Operating cash flow is the cash generated from a company's operating activities.",
    "What is free cash flow?": "Free cash flow is the cash remaining after deducting capital expenditures from operating cash flow.",
    "What is interest coverage ratio?": "Interest coverage ratio measures a company's ability to cover its interest expenses with its operating income."
}

@app.route("/chat", methods=['POST'])
def chat():
    try:
        if request.content_type != 'application/json':
            return jsonify({"response": "Unsupported Media Type: Content-Type must be application/json"}), 415

        incoming_msg = request.json.get('message', '').strip()
        app.logger.debug(f"Received message: {incoming_msg}")

        if not incoming_msg:
            return jsonify({"response": "The message is empty. Please provide a valid message."}), 400

        # البحث عن الإجابة في القاموس
        if incoming_msg in faq:
            answer = faq[incoming_msg]
        else:
            # إذا لم يكن السؤال في القاموس، اتصل بـ OpenAI API للحصول على رد ذكي
            answer = get_openai_response(incoming_msg)
        
        app.logger.debug(f"Sending response: {answer}")
        return jsonify({"response": answer})
    except Exception as e:
        app.logger.error(f"Error: {str(e)}", exc_info=True)
        return jsonify({"response": "Sorry, an error occurred. Please try again later."}), 500

def get_openai_response(message):
    try:
        # إعداد طلب OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            max_tokens=150
        )
        # استخراج النص من الرد
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        app.logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
        return "Sorry, there was an error with the OpenAI API. Please try again later."
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return "Sorry, an unexpected error occurred. Please try again later."

if __name__ == "__main__":
    app.run(debug=True)
