class GoalController < ApplicationController
	def createNewGoal
		title = params[:title];
		description = params[:description];
		tags = params[:tags];
	end
end
