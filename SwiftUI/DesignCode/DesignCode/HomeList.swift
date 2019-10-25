//
//  HomeList.swift
//  DesignCode
//
//  Created by iOS on 2019/10/25.
//  Copyright © 2019 沙睿. All rights reserved.
//

import SwiftUI

struct HomeList: View {
    @State var showContentView = false
    
    var body: some View {
        
        VStack {
            HStack {
                VStack (alignment:.leading){
                    Text("标题")
                        .font(.largeTitle)
                        .fontWeight(.heavy)
                    Text("标题2")
                        .foregroundColor(.gray)
                }
                Spacer()
            }
            .padding(.leading, 70)
            .padding(.bottom, 40)
            
            ScrollView (.horizontal ,showsIndicators: false){
                HStack (spacing: 30){
                    ForEach(courseData) { item in
                        Button(action: {
                            self.showContentView.toggle();
                        }) {
                            CourseView(title: item.title,
                                       icon: item.icon,
                                       shadowColor: item.shadowColor,
                                       color: item.color)
                            
                        }.sheet(isPresented:self.$showContentView) {
                            ContentView()
                        }
                    }
                }
                .padding(.leading, 40)
                
                Spacer()
            }
        }
        .padding(.top, 70)
    }
}

struct HomeList_Previews: PreviewProvider {
    static var previews: some View {
        HomeList()
    }
}

struct CourseView: View {
    var title = ""
    var icon = ""
    var shadowColor = ""
    var color = ""
    var body: some View {
        VStack (alignment:.leading){
            Text(title)
                .font(.title)
                .foregroundColor(Color.white)
                .fontWeight(.bold)
                .padding(20)
                .lineLimit(4)
                .padding(.trailing, 50)
            Spacer()
            Image(icon)
                .resizable()
                .renderingMode(.original)
                .aspectRatio(contentMode: .fit)
                .frame(width: 246,height: 200)
            
        }
        .background(Color(color))
        .cornerRadius(20)
        .frame(width: 246, height: 360)
        .shadow(color: Color(shadowColor), radius: 20, x: 0, y: 20)
    }
}


struct Course: Identifiable {
    var id = UUID()
    var title: String
    var icon : String
    var color: String
    var shadowColor: String
}

let courseData = [
    Course(
        title: "Hello SwiftUIHello SwiftUIHello SwiftUI",
        icon: "Illustration1",
        color: "background3",
        shadowColor: "backgroundShadow3"
    ),
    Course(
        title: "Hello SwiftUI",
        icon: "Illustration2",
        color: "background4",
        shadowColor: "backgroundShadow4"
    )
]
