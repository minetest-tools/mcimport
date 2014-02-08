local timer = 0

local function load(pos)
	local filename = minetest.get_worldpath().."/blocks/"..math.floor(pos.x/16).."."..math.floor(pos.y/16).."."..math.floor(pos.z/16)..".we"
	local pos1 = {x = math.floor(pos.x/16)*16, y = math.floor(pos.y/16)*16, z = math.floor(pos.z/16)*16}
	local pos2 = vector.add(pos1, {x=15, y=15, z=15})
	local file, err
	file, err = io.open(filename, "rb")
	if err then
		return
	end
	worldedit.set(pos1, pos2, "air")
	local content = file:read("*a")
	file:close()
	os.remove(filename)
	print(worldedit.deserialize(pos1, content))
end

minetest.register_globalstep(function(dtime)
	timer = timer + dtime
	if timer < 5 then return end
	timer = 0
	
	for _,player in ipairs(minetest.get_connected_players()) do
		local pos = player:getpos()
		
		load(pos)
		load({x=pos.x-16, y=pos.y, z=pos.z})
		load({x=pos.x, y=pos.y-16, z=pos.z})
		load({x=pos.x, y=pos.y, z=pos.z-16})
		load({x=pos.x+16, y=pos.y, z=pos.z})
		load({x=pos.x, y=pos.y+16, z=pos.z})
		load({x=pos.x, y=pos.y, z=pos.z+16})
	end
end)

minetest.register_tool("mcimport:test", {
	description = "Test",
	on_use = function(itemstack, user, pointed_thing)
		print(dump(minetest.get_node(pointed_thing.under)))
	end,
})
