//
//  Home.swift
//  DesignCode
//
//  Created by iOS on 2019/10/24.
//  Copyright © 2019 沙睿. All rights reserved.
//

import SwiftUI

struct Home: View {
    
    @State var show: Bool = false
    @State var showProfile: Bool = false
    var body: some View {
        
        ZStack {
            HomeList()
                .blur(radius: show ? 20 : 0)
                .scaleEffect(showProfile ? 0.95 : 1)
                .animation(.default)
            ContentView()
                .cornerRadius(30.0)
                .shadow(radius: 30)
                .animation(.spring())
                .offset(y: showProfile ? 40 : UIScreen.main.bounds.height)
            
            MenuButton(show: $show)
                .animation(.spring())
                .offset(x: -30 ,y: showProfile ? 0 : 80)
            
            
            MenuRight(show: $showProfile)
                .animation(.spring())
                .offset(x:-15, y: showProfile ? 0 : 88)
            
            MenuView(show: $show)
        }
        
    }
}

struct Home_Previews: PreviewProvider {
    static var previews: some View {
        Home()
    }
}

struct MenuRow: View {
    var image = "creatcard"
    var text = "My Account"
    
    var body: some View {
        HStack {
            Image(systemName:image)
                .imageScale(.large)
                .foregroundColor(Color("icons"))
                .frame(width: 32, height: 32)
                .frame(width: 32, height: 32)
            Text(text)
                .font(.headline)
            Spacer()
        }
    }
}

struct Menu : Identifiable{
    var id = UUID()
    var title : String
    var icon: String
}

let menuData = [
    Menu(title: "我的账户", icon: "person.crop.circle"),
    Menu(title: "钱包", icon: "creditcard"),
    Menu(title: "团队", icon: "person.2"),
    Menu(title: "退出", icon: "arrow.uturn.down"),
]

struct MenuView: View {
    
    var menu = menuData
    @Binding var show: Bool
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            ForEach(menu) { item in
                MenuRow(image:item.icon, text:item.title )
            }
            
            Spacer()
        }
        .padding(.top,20)
        .padding(30)
        .frame(minWidth:0, maxWidth: .infinity)
        .background(Color.white)
        .cornerRadius(30)
        .padding(.trailing,60)
        .shadow(radius: 20)
        .animation(.spring())
        .rotation3DEffect(Angle(degrees: show ? 0 : 70), axis: (x: 0, y: 10.0, z: 0))
        .offset(x: show ? 0 :-UIScreen.main.bounds.width, y:0)
        .onTapGesture {
            self.show.toggle()
        }
        
    }
}

struct CircleButton: View {
    var icon = "list.dash"
    var body: some View {
        return  HStack {
            Image(systemName:icon)
                .foregroundColor(Color.black)
        }
        .frame(width: 44, height: 44)
        .background(Color.white)
        .cornerRadius(30)
        .shadow(color: Color("buttonShadow"), radius: 10, x: 0, y: 10)
    }
}

struct MenuButton: View {
    @Binding var show : Bool
    var body: some View {
        VStack (alignment:.leading){
            HStack {
                Button(action: { self.show.toggle() }) {
                    HStack {
                        Spacer()
                        Image(systemName: "list.dash")
                            .foregroundColor(Color.black)
                    }
                    .padding(.trailing,20)
                    .frame(width: 90, height: 60)
                    .background(Color.white)
                    .cornerRadius(30)
                    .shadow(radius: 20, y: 10)
                }
                Spacer()
            }
            Spacer()
        }
    }
}

struct MenuRight: View {
    @Binding var show : Bool
    var body: some View {
        VStack (alignment:.trailing){
            HStack {
                Spacer()
                Button(action: {self.show.toggle()}) {
                    CircleButton(icon: "person.crop.circle")
                }
                Button(action: {self.show.toggle()}) {
                    CircleButton(icon: "bell")
                }
            }
            Spacer()
        }
    }
}
