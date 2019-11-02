from aiohttp import web
routes = web.RouteTableDef()

@routes.get('/calculate')
async def calculate(request):
    print("Getting request...")
    number = 12
    for _ in range(number):
        number = number * number
    return web.Response(text="Calculated..")
app = web.Application()
app.router.add_static('/download','/home', show_index= True)
app.add_routes(routes)
web.run_app(app)

