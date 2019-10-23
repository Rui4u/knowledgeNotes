//
//  ContentView.swift
//  DesignCode
//
//  Created by 沙睿 on 2019/10/23.
//  Copyright © 2019 沙睿. All rights reserved.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        ZStack {
            
            VStack {
                Text("Card Back")
                
            }
            .frame(width: 300, height: 220)
            .background(/*@START_MENU_TOKEN@*/Color.blue/*@END_MENU_TOKEN@*/)
            .cornerRadius(20)
            .shadow(radius: /*@START_MENU_TOKEN@*/10/*@END_MENU_TOKEN@*/)
            .offset(x: 0, y: -20)

//
            VStack {
                HStack {
                    VStack(alignment: .leading) {
                        Text("UI Desigin")
                            .font(.headline)
                            .fontWeight(.bold)
                            .foregroundColor(Color("accent"))
                            .padding(.top)
                        Text(/*@START_MENU_TOKEN@*/"Certificate"/*@END_MENU_TOKEN@*/)
                            .foregroundColor(.white)
                    }
                    Spacer()
                    Image("Logo")
                        .resizable()
                        .frame(width: 30.0,height: 30)
                }
                .padding(.horizontal)
                
                Spacer()
                Image("Background")
            }
            .frame(width: 340.0, height: 220)
            .background(Color.black)
            .cornerRadius(10)
            .shadow(radius: /*@START_MENU_TOKEN@*/10/*@END_MENU_TOKEN@*/)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
