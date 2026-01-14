# UAT: Phase 3 Keyword Handlers

**Date:** 2025-12-31
**Bead:** solutions-hgwx.3
**Tester:** _______________

## Prerequisites

1. [ ] API keys configured in environment:
   - `OPENWEATHERMAP_API_KEY` - Get free key at https://openweathermap.org/api
   - `ALPHAVANTAGE_API_KEY` - Get free key at https://www.alphavantage.co/support/#api-key
   - `NEWSAPI_KEY` - Get free key at https://newsapi.org/register

2. [ ] Backend deployed with new code
3. [ ] @eis bot user exists and notification poller is running

---

## Test 1: Weather Command

### 1.1 Basic Weather
**Action:** Create task with title: `@eis !weather San Francisco`

**Expected:**
- [ ] Task is processed within ~10 seconds
- [ ] Task **stays visible** (NOT deleted)
- [ ] Title cleaned to "San Francisco" or "Weather Info"
- [ ] Response contains weather icon (☀️, ⛅, 🌧️, etc.)
- [ ] Shows temperature in °F and °C
- [ ] Shows humidity and wind speed
- [ ] Shows timestamp: "*Updated: 3:45 PM*" (or similar)
- [ ] Shows clickable **Refresh** link (🔄 [**Refresh**](url))

**Actual result:** _________________

### 1.2 Weather with Location
**Action:** Create task: `@eis !w London,UK`

**Expected:**
- [ ] Shows weather for London, UK
- [ ] Country code appears in output
- [ ] Shows clickable **Refresh** link

**Actual result:** _________________

### 1.3 Weather - Pipe to Project
**Action:** Create task: `@eis !weather Seattle | Inbox`

**Expected:**
- [ ] New task created in "Inbox" project with Seattle weather
- [ ] Original command task is deleted
- [ ] New task title: "Seattle" or "Weather Info"

**Actual result:** _________________

### 1.4 Weather - Invalid Project
**Action:** Create task: `@eis !weather Portland | NonexistentProject`

**Expected:**
- [ ] Task updated in place (not moved)
- [ ] Warning: "Project 'NonexistentProject' not found"

**Actual result:** _________________

### 1.5 Weather - Invalid Location
**Action:** Create task: `@eis !weather InvalidCity12345XYZ`

**Expected:**
- [ ] Error message: "Location not found"
- [ ] Task gets error comment (not deleted)

**Actual result:** _________________

### 1.6 Weather - No API Key (if testing locally)
**Action:** Temporarily unset `OPENWEATHERMAP_API_KEY` and create task: `@eis !w`

**Expected:**
- [ ] Error: "Weather API not configured"

**Actual result:** _________________

---

## Test 2: Stock Command

### 2.1 Basic Stock Quote
**Action:** Create task: `@eis !stock AAPL`

**Expected:**
- [ ] Task stays visible (not deleted)
- [ ] Shows current price with $ symbol
- [ ] Shows change amount and percentage
- [ ] Icon: 📈 (up) or 📉 (down) or ➖ (flat)
- [ ] Shows Open/High/Low/Volume

**Actual result:** _________________

### 2.2 Stock with Alias
**Action:** Create task: `@eis !s MSFT`

**Expected:**
- [ ] Same format as above for Microsoft

**Actual result:** _________________

### 2.3 Stock - Pipe to Project
**Action:** Create task: `@eis !s GOOGL | Dashboard`

**Expected:**
- [ ] New task created in "Dashboard" project
- [ ] Original task deleted

**Actual result:** _________________

### 2.4 Stock - Invalid Ticker
**Action:** Create task: `@eis !stock INVALIDTICKER999`

**Expected:**
- [ ] Error: "No data found for ticker"

**Actual result:** _________________

### 2.5 Stock - No Ticker Provided
**Action:** Create task: `@eis !stock`

**Expected:**
- [ ] Error: "No ticker symbol provided"

**Actual result:** _________________

---

## Test 3: News Command

### 3.1 General Headlines
**Action:** Create task: `@eis !news`

**Expected:**
- [ ] Task stays visible (not deleted)
- [ ] Shows 📰 **Headlines** header
- [ ] Lists 5 news articles with titles
- [ ] Each article has source name
- [ ] Titles are clickable links

**Actual result:** _________________

### 3.2 News with Search Query
**Action:** Create task: `@eis !news technology`

**Expected:**
- [ ] Headlines related to "technology"
- [ ] Header shows: **Headlines: technology**

**Actual result:** _________________

### 3.3 News with Category
**Action:** Create task: `@eis !n category:sports`

**Expected:**
- [ ] Sports-related headlines
- [ ] Header shows: **Sports Headlines**

**Actual result:** _________________

### 3.4 News - Pipe to Project
**Action:** Create task: `@eis !news | Inbox`

**Expected:**
- [ ] News task created in Inbox project
- [ ] Original command task deleted

**Actual result:** _________________

### 3.5 News Alias
**Action:** Create task: `@eis !headlines business`

**Expected:**
- [ ] Business news headlines

**Actual result:** _________________

---

## Test 4: Scheduled Updates

### 4.1 Weather with Schedule
**Action:** Create task: `@eis !weather NYC / every morning at 7am`

**Expected:**
- [ ] Shows current weather
- [ ] Footer: "🔄 *Auto-updating: every morning at 7am*"
- [ ] Footer: "⏰ *Next refresh: 7:00 AM*" (or "tomorrow 7:00 AM")
- [ ] Shows clickable **Refresh** link

**Actual result:** _________________

### 4.2 Weather with Interval Schedule
**Action:** Create task: `@eis !w Seattle / every 30 minutes`

**Expected:**
- [ ] Shows current weather
- [ ] Footer: "🔄 *Auto-updating: every 30 minutes*"
- [ ] Footer: "⏰ *Next refresh: in 30 min*"

**Actual result:** _________________

### 4.3 Stock with Schedule
**Action:** Create task: `@eis !s GOOGL / hourly`

**Expected:**
- [ ] Shows current stock price
- [ ] Footer: "🔄 *Auto-updating: hourly*"

**Actual result:** _________________

---

## Test 5: Clickable Refresh

### 5.1 Click Refresh Link
**Action:**
1. Create task: `@eis !weather Denver`
2. Wait for weather to appear
3. Click the **Refresh** link in the task description

**Expected:**
- [ ] Browser opens the refresh URL
- [ ] Weather is refreshed with new data
- [ ] Redirects back to task in Vikunja
- [ ] Timestamp updates to current time

**Actual result:** _________________

### 5.2 Refresh Link Security
**Action:**
1. Copy a refresh URL from a weather task
2. Change the task ID in the URL
3. Try to access the modified URL

**Expected:**
- [ ] Returns 401 error "Invalid or expired refresh token"
- [ ] Does NOT refresh the wrong task

**Actual result:** _________________

---

## Test 6: Fuzzy Matching

### 6.1 Typo in Weather
**Action:** Create task: `@eis !wether Seattle`

**Expected:**
- [ ] Still matches to weather handler
- [ ] Shows Seattle weather

**Actual result:** _________________

### 6.2 Typo in News
**Action:** Create task: `@eis !newz`

**Expected:**
- [ ] Still matches to news handler
- [ ] Shows headlines

**Actual result:** _________________

---

## Test 7: Rate Limiting

### 7.1 Weather Rate Limit
**Note:** Weather API limited to 500 calls/day (50% safety margin)

**Action:** Check rate limit status after multiple calls

**Expected:**
- [ ] Successful calls are counted
- [ ] When limit reached: "Daily API limit reached (500/500 calls)"

**Actual result:** _________________

### 7.2 Stock API Rate Limit
**Note:** Alpha Vantage free tier is 5 calls/minute

**Action:** Rapidly create 6+ stock tasks

**Expected:**
- [ ] First 5 succeed
- [ ] 6th shows: "API rate limit reached"

**Actual result:** _________________

---

## Summary

| Feature | Pass | Fail | Notes |
|---------|------|------|-------|
| Weather - Basic (task stays) | | | |
| Weather - Timestamp | | | |
| Weather - Clickable Refresh | | | |
| Weather - Pipe syntax | | | |
| Weather - Schedule + next | | | |
| Stock - Basic | | | |
| Stock - Pipe syntax | | | |
| News - General | | | |
| News - Pipe syntax | | | |
| Clickable Refresh | | | |
| Refresh Link Security | | | |
| Fuzzy Matching | | | |
| Rate Limiting | | | |

**Overall Result:** [ ] PASS  [ ] FAIL

**Issues Found:**
1. _________________
2. _________________
3. _________________

**Sign-off:** _______________  Date: _______________
