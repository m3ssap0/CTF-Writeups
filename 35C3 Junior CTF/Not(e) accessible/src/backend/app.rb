require 'sinatra'
set :bind, '0.0.0.0'

get '/get/:id' do
	File.read("./notes/#{params['id']}.note")
end

get '/store/:id/:note' do 
	File.write("./notes/#{params['id']}.note", params['note'])
	puts "OK"
end 

get '/admin' do
	File.read("flag.txt")
end
