## ✅ Demo Output

After running the container, you can confirm it's working with:

```bash
curl http://localhost:8000
It should return:

json
Copy
Edit
{"message": "Hello, world"}
Alternatively, here’s a screenshot of the actual output:


yaml
Copy
Edit

---

## 🥉 Step 3：Gitに追加してGitHubにPush

以下のコマンドを順に実行してください（画像とREADMEがGitに反映されます）：

```bash
git add README.md docs/curl-result.png
git commit -m "Add curl output screenshot and update README"
git push origin main