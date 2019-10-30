from aiohttp import web
app = web.Application()
app.router.add_static('/download','/home', show_index= True)
web.run_app(app)

