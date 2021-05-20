from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class IndexView(TemplateView):

    template_name = 'story/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['chapter'] = "1st"
        ctx['items'] = 'item'
        return ctx


class First(TemplateView):

    template_name = 'story/prologue.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['chapter'] = "1st"
        ctx['title'] = "The Fixed World"
        ctx['sub_title'] = "失われた 時 の世界"
        ctx['items'] = 'item'
        ctx['story'] = """\
幾千年も昔。
この世界の片隅、ひとつの街に、"時"を自由自在に操る民族がいたと云う。
言い伝えによれば、時を進める事も、戻すことも、…またその影響範囲さえも彼らの意図通りだった。

【在るものを無かった事】に出来る特別な力を持つ民族。
かつての人は皆、彼らのことを【時の魔術師】と呼んだ。

だが今となっては昔の話、その血は薄れ、時の魔法を使える人間は居なくなってしまったそうだ。
――ただ、今尚彼らの身に着けていた装身具を着用する文化は根強く、
この街に住む皆が、いづれかの装身具を手にしているという。

いつか戻る、その力を信じて――…

Fの世界　第１章　The Fixed　World

　－失われた時の世界－
"""
        return ctx


STORY_CONTENTS_HTML = """\
<p style="word-break: break-all;" class="story-contents">{story}</p>
"""


class Second(TemplateView):

    template_name = 'story/prologue.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['chapter'] = "2nd"
        ctx['title'] = "The Flickers Story"
        ctx['sub_title'] = ""
        ctx['items'] = 'item'
        ctx['story'] = """\
遠い遠い場所にある、まだ魔法が当たり前に存在する世界の物語。

自然豊かなこの星に、一人の青年が居た。
一所に居を構えず、世界各地を旅するトレジャーハンター。

彼の名は、カイル・オーウェン

相棒は、　「碧の短剣」

この世界には、七色に光る湖や森に棲まう水晶が道標となるラミアの森が存在する。
勿論危険は伴うが、見るものを楽しませてくれる、――それだけでも旅をする理由になるだろう。


一見平和そうに見えるこの世界を、黒い影が蝕み始めていた。
もう誰にも止めることが出来ないこの現象に、彼と、その仲間たちは巻き込まれていく。

…そしてもうひとつ。
今となっては当たり前のこととなっていて誰も気に留めてはいないが、
この世界には、遠い昔から存在する


――空に浮かぶ大きな大陸があった。


Fの世界　第Ⅱ章　 ～　The Flicker's  Story　～

"""
        return ctx


class Third(TemplateView):

    template_name = 'story/prologue.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['chapter'] = "3rd"
        ctx['title'] = "Magical Fantasy"
        ctx['sub_title'] = "失われた 時 の世界"
        ctx['items'] = 'item'
        ctx['story'] = """\
遠い遠い場所にある、まだ魔法が当たり前に存在する世界の物語。

自然豊かなこの星に、一人の青年が居た。
一所に居を構えず、世界各地を旅するトレジャーハンター。

彼の名は、カイル・オーウェン

相棒は、　「碧の短剣」

この世界には、七色に光る湖や森に棲まう水晶が道標となるラミアの森が存在する。
勿論危険は伴うが、見るものを楽しませてくれる、――それだけでも旅をする理由になるだろう。


一見平和そうに見えるこの世界を、黒い影が蝕み始めていた。
もう誰にも止めることが出来ないこの現象に、彼と、その仲間たちは巻き込まれていく。

…そしてもうひとつ。
今となっては当たり前のこととなっていて誰も気に留めてはいないが、
この世界には、遠い昔から存在する


――空に浮かぶ大きな大陸があった。


Fの世界　第Ⅱ章　 ～　The Flicker's  Story　～

"""
        return ctx

class MainView(TemplateView):

    template_name = "html/index.html"

    def get_context_data(self, **kwargs):

        return None