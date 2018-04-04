class CreateGoals < ActiveRecord::Migration[5.0]
  def change
    create_table :goals do |t|
      t.string :title
      t.text :description
      t.string :tags
      t.datetime :time
      t.string :projects
      t.string :comments
      t.string :followers

      t.timestamps
    end
  end
end
