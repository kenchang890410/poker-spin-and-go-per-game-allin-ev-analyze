# Poker Spin and Gold per Game Allin EV Analyzer

這個程式可以分析德州撲克平台 Natural8 的 spin and gold 遊戲結果，計算玩家遊戲中 allin 之後籌碼獲得的期望值。

撲克模擬發牌與讀取計算期望值使用 treys、random 函式庫，最後畫圖顯示標準差使用 matplotlib 函式庫。

spin and gold 這個遊戲方式的策略中包含大量 allin 的動作，時機的選擇是一個重要的關鍵。

德州撲克這個遊戲有著極高的波動，也就是即使做了錯誤的決定也有可能獲得好的結果，反之正確決定不一定 100% 營利。

所以通過這個程式可以分析到玩家選擇 allin 的正確與否，期望值是不是高的，藉此可以讓玩家自己知道當營利時是運氣好，還是正確的決定。

## 輸入使用方法

點開遊戲內戰績按鈕連結到 PokerCraft 戰績分析網站，接著點黃金&轉盤進到畫面如下圖

![image](https://github.com/kenchang890410/poker-spin-and-go-per-game-allin-ev-analyze/blob/aba5c142076a7ce9fe9a4bcc75053515c59b326f/PokerCraft.png)

接著點擊右上角紅色下載遊戲歷史紀錄，放置到自訂資料夾並且把程式內 directory 修改成資料夾路徑

## 輸出結果介紹

測試輸入為 input 資料夾下 81 場遊戲資訊

total_ev :  -965.3285999999997 //總期望價值 EV

total_profit_chip :  1693.0 //總實際籌碼營利

total_allin_game_count :  169 //總 allin 次數

all_pot_size_sum :  43460.0 //總底池大小

total_all_in_winrate :  0.48889405660377355 //理論 EV 勝率

all_in_winrate result:  0.5194776806258629 //實際結果勝率

AVG pot size :  257.15976331360946 //平均底池大小

reality win game count :  6.583456051541647 //實際結果贏平均底池局數

ev win game count :  -3.753808867924527 //理論 EV 贏平均底池局數

target_win :  87 //目標贏局數

Probability of exactly 87 wins: 0.048873 //達到目標贏局概率

Mean : 82.6231 //平均應贏得局數

Standard Deviation : 6.4984 //標準差

87 wins is 0.6735 standard deviations away from the mean. //Z-Score

最終會輸出圖表示理論上最可能出現的贏局次數分佈。如下圖

![image](https://github.com/kenchang890410/poker-spin-and-go-per-game-allin-ev-analyze/blob/1e6f32cd6a0bcf6761d530511e327004fff93010/distribution.png)
