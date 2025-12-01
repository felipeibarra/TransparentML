#!/bin/bash

echo "=========================================="
echo "🔍 Timeline Deployment Verification"
echo "=========================================="
echo ""

echo "1️⃣  Checking if timeline files exist in container..."
docker exec transparentml-url-diagnostics ls -lh /app/static/timeline.html 2>/dev/null
docker exec transparentml-url-diagnostics ls -lh /app/static/js/timeline-enhanced.js 2>/dev/null
docker exec transparentml-url-diagnostics ls -lh /app/static/css/timeline-enhanced.css 2>/dev/null
echo ""

echo "2️⃣  Checking if timeline button exists in dashboard..."
if docker exec transparentml-url-diagnostics grep -q "timelineBtn" /app/static/dashboard.html; then
    echo "✅ Timeline button found in dashboard.html"
else
    echo "❌ Timeline button NOT found in dashboard.html"
fi
echo ""

echo "3️⃣  Checking if btn-info CSS exists..."
if docker exec transparentml-url-diagnostics grep -q "btn-info" /app/static/css/dashboard.css; then
    echo "✅ btn-info style found in dashboard.css"
else
    echo "❌ btn-info style NOT found in dashboard.css"
fi
echo ""

echo "4️⃣  Testing /timeline endpoint..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8003/timeline)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ /timeline endpoint responding (HTTP $HTTP_CODE)"
else
    echo "❌ /timeline endpoint error (HTTP $HTTP_CODE)"
fi
echo ""

echo "5️⃣  Testing dashboard root..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8003/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Dashboard responding (HTTP $HTTP_CODE)"
else
    echo "❌ Dashboard error (HTTP $HTTP_CODE)"
fi
echo ""

echo "6️⃣  Checking if button is served in HTTP response..."
if curl -s http://localhost:8003/ | grep -q "timelineBtn"; then
    echo "✅ Timeline button is being served in HTTP response"
else
    echo "❌ Timeline button NOT in HTTP response"
fi
echo ""

echo "=========================================="
echo "📋 Summary"
echo "=========================================="
echo ""
echo "Dashboard URL:  http://localhost:8003/"
echo "Timeline URL:   http://localhost:8003/timeline"
echo ""
echo "⚠️  If you don't see the button in your browser:"
echo "   1. Hard refresh: Cmd + Shift + R (Mac) or Ctrl + Shift + R (Windows/Linux)"
echo "   2. Clear browser cache"
echo "   3. Try in incognito/private window"
echo ""
