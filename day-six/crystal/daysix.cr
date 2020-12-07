content = File.open("../data-axiom.txt") do |file|
    file.gets_to_end
end

groups = content.split(/\n\n/)
responses_by_group = groups.map { |x| x.split(/\n/) }
response_sets_by_group = responses_by_group.map {|g| g.map { |s| s.chars.to_set }}

each = response_sets_by_group.map {|s| s.reduce { |m, i| m | i} }
every = response_sets_by_group.map {|s| s.reduce { |m, i| m & i} }

puts each.map{ |g| g.size }.reduce {|m,i| m + i}
puts every.map{ |g| g.size }.reduce {|m,i| m + i}