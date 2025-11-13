# How to Get API Keys for AI Code Reviewer

The AI Code Reviewer works in **mock mode** by default - no API keys required! However, for full AI-powered analysis with advanced capabilities, you can integrate with either Anthropic Claude or OpenAI GPT.

## Table of Contents

1. [Do I Need an API Key?](#do-i-need-an-api-key)
2. [Getting an Anthropic Claude API Key](#getting-an-anthropic-claude-api-key-recommended)
3. [Getting an OpenAI API Key](#getting-an-openai-api-key-alternative)
4. [Configuring Your API Key](#configuring-your-api-key)
5. [Cost Considerations](#cost-considerations)
6. [Troubleshooting](#troubleshooting)

---

## Do I Need an API Key?

**Short answer: No!**

The AI Code Reviewer includes a sophisticated **mock mode** that:
- ✅ Detects programming languages
- ✅ Performs static code analysis
- ✅ Identifies security vulnerabilities
- ✅ Calculates quality metrics
- ✅ Provides smart suggestions

**With an API key, you get:**
- 🤖 Deep contextual understanding
- 🤖 Framework-specific recommendations
- 🤖 Advanced refactoring suggestions
- 🤖 More nuanced security analysis
- 🤖 Natural language explanations

---

## Getting an Anthropic Claude API Key (Recommended)

Anthropic Claude is recommended for this project as it excels at code analysis and understanding.

### Step 1: Create an Anthropic Account

1. Go to [https://www.anthropic.com](https://www.anthropic.com)
2. Click **"Get API Access"** or **"Console"**
3. Sign up with your email address
4. Verify your email

### Step 2: Access the API Console

1. Log in to the [Anthropic Console](https://console.anthropic.com)
2. Navigate to **"API Keys"** in the sidebar

### Step 3: Generate an API Key

1. Click **"Create Key"**
2. Give your key a descriptive name (e.g., "AI Code Reviewer - Local Dev")
3. Click **"Create"**
4. **Important**: Copy the key immediately! You won't be able to see it again.

Your key will look like: `sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 4: Add Credits (If Required)

- Anthropic may require you to add payment information
- New accounts often get free trial credits
- Check [Anthropic's pricing](https://www.anthropic.com/pricing) for current rates

### Pricing

As of 2024:
- **Claude 3.5 Sonnet**: ~$3 per million input tokens, ~$15 per million output tokens
- A typical code review uses 500-2000 tokens
- **Estimated cost**: $0.002 - $0.01 per review

---

## Getting an OpenAI API Key (Alternative)

OpenAI GPT-4 is also supported and provides excellent code analysis capabilities.

### Step 1: Create an OpenAI Account

1. Go to [https://platform.openai.com](https://platform.openai.com)
2. Click **"Sign up"**
3. Create an account with your email or Google/Microsoft account
4. Verify your email

### Step 2: Access API Keys

1. Log in to [OpenAI Platform](https://platform.openai.com)
2. Click your profile icon (top right)
3. Select **"View API Keys"**

### Step 3: Generate an API Key

1. Click **"Create new secret key"**
2. Name your key (e.g., "AI Code Reviewer")
3. Click **"Create secret key"**
4. **Important**: Copy the key immediately! You won't be able to see it again.

Your key will look like: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 4: Add Billing Information

1. Go to **"Billing"** → **"Payment methods"**
2. Add a payment method
3. Set usage limits (recommended for safety)

### Pricing

As of 2024:
- **GPT-4**: ~$30 per million input tokens, ~$60 per million output tokens
- **GPT-3.5 Turbo**: ~$0.50 per million input tokens, ~$1.50 per million output tokens
- A typical code review uses 500-2000 tokens
- **Estimated cost**: $0.015 - $0.12 per review (GPT-4)

---

## Configuring Your API Key

### Step 1: Create/Edit `.env` File

In the project root directory:

```bash
# If .env doesn't exist, copy from example
cp .env.example .env

# Edit the file
nano .env
# or
code .env
```

### Step 2: Add Your API Key

**For Anthropic Claude:**

```env
# LLM Configuration
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=4096
```

**For OpenAI:**

```env
# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-key-here
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=4096
```

### Step 3: Restart the Application

**If using Docker:**

```bash
docker-compose down
docker-compose up -d
```

**If running manually:**

- Stop the backend server (Ctrl+C)
- Restart it: `PYTHONPATH=. uvicorn api.main:app --reload`

### Step 4: Verify It's Working

1. Go to [http://localhost:3000](http://localhost:3000)
2. Submit a code review
3. Look for AI-powered insights (not mock mode messages)

You should see detailed, context-aware analysis instead of the mock mode message.

---

## Cost Considerations

### Monitoring Usage

**Anthropic:**
1. Go to [Anthropic Console](https://console.anthropic.com)
2. Check **"Usage"** section
3. Set up billing alerts

**OpenAI:**
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Navigate to **"Usage"**
3. Set up usage limits under **"Billing"** → **"Limits"**

### Cost-Saving Tips

1. **Use Mock Mode for Development**
   - Only enable AI for production or important reviews
   - Mock mode is free and fast

2. **Set Usage Limits**
   - Set monthly spending limits in your API dashboard
   - This prevents unexpected charges

3. **Choose the Right Model**
   - GPT-3.5 Turbo is cheaper than GPT-4
   - Claude Haiku is cheaper than Claude Sonnet

4. **Optimize Prompts**
   - The application is optimized to use minimal tokens
   - Avoid reviewing very large files unnecessarily

5. **Use Caching**
   - Review similar code together
   - Some providers offer prompt caching

### Free Tiers & Credits

- **Anthropic**: Often provides trial credits for new users
- **OpenAI**: May provide initial credits (check current promotions)
- **Both**: Offer educational or research discounts in some cases

---

## Troubleshooting

### "Invalid API Key" Error

**Check:**
1. Key is correctly copied (no extra spaces)
2. Key starts with correct prefix (`sk-ant-` or `sk-`)
3. Key hasn't been deleted or revoked
4. You're using the correct provider setting

### "Rate Limit Exceeded" Error

**Solutions:**
1. Wait a few moments and try again
2. Check if you've hit your account's rate limit
3. Upgrade your plan if needed
4. Temporarily use mock mode

### "Insufficient Credits" Error

**Solutions:**
1. Add payment method to your account
2. Purchase more credits
3. Check if free trial has expired
4. Use mock mode while resolving

### Backend Not Using API Key

**Check:**
1. `.env` file is in the project root directory (not in backend/ or frontend/)
2. Environment variables are correctly formatted (no quotes around values)
3. Backend was restarted after adding the key
4. No typos in variable names (`ANTHROPIC_API_KEY` not `ANTHROPIC_KEY`)

### Cost Concerns

**If costs are higher than expected:**
1. Check usage dashboard for unexpected activity
2. Revoke and regenerate your API key
3. Set strict usage limits
4. Switch to mock mode temporarily

---

## Best Practices

### Security

1. **Never commit API keys to Git**
   - The `.env` file is in `.gitignore`
   - Double-check before pushing code

2. **Use environment-specific keys**
   - Development key for local testing
   - Production key for deployed app
   - Different keys for different team members

3. **Rotate keys regularly**
   - Change keys every 3-6 months
   - Immediately rotate if compromised

4. **Monitor usage**
   - Set up alerts for unusual activity
   - Review usage weekly

### Development

1. **Start with mock mode**
   - Test features without costs
   - Switch to AI only when needed

2. **Use AI for complex code**
   - Simple code: Mock mode is sufficient
   - Complex/critical code: Use AI

3. **Test both modes**
   - Ensure your code works with and without AI
   - Graceful degradation if API is down

---

## Additional Resources

### Anthropic
- [API Documentation](https://docs.anthropic.com/)
- [Pricing](https://www.anthropic.com/pricing)
- [Best Practices](https://docs.anthropic.com/claude/docs/best-practices)

### OpenAI
- [API Documentation](https://platform.openai.com/docs)
- [Pricing](https://openai.com/pricing)
- [Best Practices](https://platform.openai.com/docs/guides/production-best-practices)

---

## FAQ

**Q: Which provider is better?**
A: Both are excellent. Anthropic Claude is slightly better for code understanding, OpenAI has broader availability.

**Q: Can I switch providers later?**
A: Yes! Just change `LLM_PROVIDER` in `.env` and add the corresponding API key.

**Q: Is my code sent to the API?**
A: Only the code snippet you're reviewing. No other project data is sent.

**Q: Can I use both providers?**
A: Not simultaneously, but you can configure both and switch between them.

**Q: What if I exceed my budget?**
A: Set hard limits in your API dashboard. The app will gracefully fall back to mock mode on API errors.

---

**Ready to supercharge your code reviews with AI?** Follow the steps above and start analyzing! 🚀
