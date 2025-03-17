import pyxel
'''
マシュマロロード 長いぐるぐるのマシュマロ
流れてくるもの ケーキ プリン ドーナッツ マカロン
'''
GAME_TITLE = "SMEERUN"


class jumpgame:

    game_state = "TITLE"

    def __init__(self):
        # 初期設定
        pyxel.init(160, 120, title=GAME_TITLE)

        # 画像読み込み
        pyxel.load("jumpgame.pyxres")

        # 色変更 https://kinutani.hateblo.jp/entry/2022/12/18/224843
        # pyxel.colors[0] = 黒
        pyxel.colors[1] = 0x353535 # 濃いグレー(服のグレー部分)
        # pyxel.colors[2] = 
        pyxel.colors[3] = 0xB3B294 # 髪の影色
        pyxel.colors[4] = 0xafeeee # マシュマロの青
        # pyxel.colors[5] = 
        #pyxel.colors[6] = 
        # pyxel.colors[7] = 白
        # pyxel.colors[8] = 濃いピンク(透過色)
        pyxel.colors[9] = 0xAA71B6 # 紫(目の色)
        # pyxel.colors[10] = 黄色
        pyxel.colors[11] = 0xCCCBB6 # ライトモスグリーン(髪の色)
        pyxel.colors[12] = 0x7A7869 # (みるく茶)顔の周りの線
        # pyxel.colors[13] = 薄い茶色(袖)
        pyxel.colors[14] = 0xF7CFCF # ほっぺの色
        pyxel.colors[15] = 0xFCEDE6 #肌色

        # 初期状態はタイトル画面。title play resultというつの状態が存在する。
        self._game_state = "TITLE"

        # スミー
        self.smee_sprite = [
            (20, 51, 0, 0, 0, 24, 32, 8), # 待機モーション1
            (20, 50, 0, 24, 0, 24, 33, 8), # 待機モーション2
            (20, 48, 0, 48, 0, 24, 30, 8), # 走りモーション1
            (19, 48, 0, 72, 0, 25, 30, 8), # 走りモーション2
            (15, 62, 0, 132, 0, 35, 25, 8), # スライディングモーション1
            (19, 62, 0, 168, 0, 31, 25, 8), # スライディングモーション2
            (20, 35, 0, 104, 0, 28, 35, 8) # ジャンプモーション
        ]
        self.name = "SMEE"

        self.mash =0
        self.frame = 0
        self.play_score = 0 # ゲームスコア
        
        self.player = player(self)
        self.sweets = sweets(self)

        pyxel.mouse(True)

        # 処理
        pyxel.run(self.update, self.draw)
    
    @property
    def game_state(self):
        return self._game_state
    
    @game_state.setter
    def game_state(self, set_game_state):
        self._game_state = set_game_state

    # アプリを更新する
    def update(self):

        # プレイヤーのアップデート
        self.player.update()
        
        if self._game_state == "TITLE":
            pass
            
        if self._game_state == "PLAY":

            # スイーツのアップデート
            self.sweets.update()

            # 30フレームごとに1ポイント
            if pyxel.frame_count % 30 == 0:
                self.play_score += 1

            # 長いマシュマロの処理
            if self.mash == -51:
                self.mash = 0
            self.mash -= 3
                    
        elif self._game_state == "RESULT":
            pass


    # アプリを描画する
    def draw(self):
        pyxel.cls(5)

        # キャラの描画
        self.player.draw()

        if self._game_state == "TITLE":
            pyxel.text(70, 60, self.player.name + "RUN", 10)
            pyxel.text(62, 70, "press space", 9)

        if self._game_state == "PLAY":
            pyxel.text(3, 3, "SCORE:", 10)
            pyxel.text(28, 3, str(self.play_score), 10)

            # 長いマシュマロ
            for i in range(5):
                pyxel.blt(self.mash + i*48, 83, 1, 0, 0, 48, 16, 8)

            # 体力(ビスケット)
            pyxel.blt(150, 3, 2, 0, 16, 8, 8, 8)
            pyxel.blt(140, 3, 2, 0, 16, 8, 8, 8)
            pyxel.blt(130, 3, 2, 0, 16, 8, 8, 8)

            # スイーツのアップデート
            self.sweets.draw()

            # ジャンプのクールタイムバー
            if self.player.after_jump_frame > 0:
                pyxel.blt(25, 85, 0, 200, 0, self.player.after_jump_frame -1 , 3, 8)


class player:
    def __init__(self, game):
        self.anime = 0
        self._after_jump_frame = 0
        self.frame = 0
        self.game = game
        self.sprite = self.game.smee_sprite
        self.name = self.game.name
        self.attack = False
        self.is_space_released = False

    def idle(self):
        # アニメーション処理
        if self.frame == 13:
            # self.animeが0なら1、1なら0になる
            self.anime = 1 - self.anime
            self.frame = 0

        if self.anime == 0:
            # 待機モーション1
            self.sprite_info = self.sprite[0]
            
        elif self.anime == 1:
            # 待機モーション2
            self.sprite_info = self.sprite[1]

        if self.is_space_released and pyxel.btnp(pyxel.KEY_SPACE):
            self.ps_state = "run"
            self.mash = 0
            self.is_space_released = False  # スペースキーの状態をリセット
            self.game.game_state = "PLAY"

        

    def jump(self):

        # ジャンプモーション
        self.sprite_info = (20, 35, 0, 104, 0, 28, 35, 8)

        if self.frame == 15:
            pyxel.stop(0)
            self.ps_state = "run"
            self.frame = 0
            self.after_jump_frame = 15

    @property
    def after_jump_frame(self):
        return self._after_jump_frame
    
    @after_jump_frame.setter
    def after_jump_frame(self, set_after_jump_frame):
        self._after_jump_frame = set_after_jump_frame

    def slide(self):

        self.frame += 1

        if self.frame < 5:
            # アタックモーション #smee_slide1
            self.sprite_info = (15, 62, 0, 132, 0, 35, 25, 8)
            # アタック判定をTRUEにする
            self.attack = True

        else:
            # アタック判定をFALSEにする #smee_slide2
            self.attack = False
            self.sprite_info = (19, 62, 0, 168, 0, 31, 25, 8)
            pass

        if pyxel.btnr(pyxel.KEY_SPACE) or self.frame == 40:
            self.frame = 0
            pyxel.stop(0) # チャンネル0の音声のみ停止
            pyxel.play(0, 1) # ジャンプの効果音
            self.attack = False
            self.ps_state = "jump"

    def run(self): # 走っているときの処理

        # ジャンプのクールタイム
        if self.after_jump_frame != 0:
            self.after_jump_frame -= 1
        
        # アニメーション処理
        if self.frame == 1:
            # 走りモーション1 smee_run1
            self.sprite_info = (20, 48, 0, 48, 0, 24, 30, 8)

        elif self.frame == 4 or self.frame == 10:
            # 待機モーション2 smee_idle2
            self.sprite_info = (20, 50, 0, 24, 0, 24, 33, 8)
            pyxel.play(0, 2)

        elif self.frame == 7:
            # 走りモーション2 smee_run2
            self.sprite_info = (19, 48, 0, 72, 0, 25, 30, 8)

        elif self.frame == 13:
            self.frame = 0

        # ボタン処理
        if self.is_space_released and pyxel.btnp(pyxel.KEY_SPACE) and self.after_jump_frame == 0: # , hold=30, repeat=2
            self.ps_state = "slide"
            pyxel.play(0, 0) # スライドの効果音
            self.frame = 0
            self.is_space_released = False   #スペースキーの状態をリセット

    def update(self):
        self.frame += 1 # プレイヤーフレーム変数に＋1
        # スペースキーが離されたことを確認する
        if not pyxel.btn(pyxel.KEY_SPACE):
            self.is_space_released = True  # 離されたことを記録

        if self.game.game_state == "TITLE":
            self.idle()

        elif self.game.game_state == "PLAY":
                if self.ps_state == "jump": 
                    self.jump()

                if self.ps_state == "slide":
                    self.slide()

                if self.ps_state == "run":
                    self.run()

        elif self.game.game_state == "RESULT":
            pass

        

    def draw(self):
        # 画面の（50，50）の位置に
        # イメージバンク「0」の（0，0）の位置から
        # 横8、縦8の範囲を描画し、カラーコード「0」（黒）は透過させる。
        pyxel.blt(*self.sprite_info)

class sweets:
    def __init__(self, game):
        self.x = 161
        self.y = 68

    def update(self):
        if self.x == -16:
            self.x = 161
        self.x -= 3

    def draw(self):
        pyxel.blt(self.x, self.y, 2, 0, 0, 15, 15, 8)

game = jumpgame()
