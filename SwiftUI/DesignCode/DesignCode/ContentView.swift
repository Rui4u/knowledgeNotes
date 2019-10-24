//
//  ContentView.swift
//  DesignCode
//
//  Created by 沙睿 on 2019/10/23.
//  Copyright © 2019 沙睿. All rights reserved.
//

import SwiftUI

struct ContentView: View {
    @State var show = false
    @State var viewState = CGSize.zero
    var body: some View {
        ZStack {
            
            TitleView()
                .blur(radius: show ? 20 : 0)
                .animation(.default)
             
            CardBottomView()
                .blur(radius: show ? 20 : 0)
                .animation(.default)
            CardView()
                .background(show ? Color.red : Color("background9"))
                .cornerRadius(20)
                .shadow(radius: /*@START_MENU_TOKEN@*/10/*@END_MENU_TOKEN@*/)
                .offset(x: 0, y: show ? -400 : -40)
                .scaleEffect(0.85)
                .rotationEffect(Angle(degrees: show ? 15.0: 0))
//                .rotation3DEffect(Angle(degrees: show ? 50 : 0), axis: /*@START_MENU_TOKEN@*/(x: 10.0, y: 10.0, z: 10.0)/*@END_MENU_TOKEN@*/)
                .animation(Animation.easeInOut(duration:0.7))
                .blendMode(.hardLight)
                .offset(x:viewState.width,y:viewState.height)
            
            CardView()
                .background(show ? Color("background5") : Color("background8"))
                .cornerRadius(20)
                .shadow(radius: /*@START_MENU_TOKEN@*/10/*@END_MENU_TOKEN@*/)
                .offset(x: 0, y: show ? -200 : -20)
                .scaleEffect(0.9)
                .animation(Animation.easeInOut(duration: 0.5))
                .rotationEffect(Angle(degrees: show ? 10: 0))
//                .rotation3DEffect(Angle(degrees: show ? 40: 0), axis: /*@START_MENU_TOKEN@*/(x: 10.0, y: 10.0, z: 10.0)/*@END_MENU_TOKEN@*/)
                .blendMode(.hardLight)
                .offset(x:viewState.width,y:viewState.height)
            
            CertificateView()
                .offset(x:viewState.width,y:viewState.height)
                .scaleEffect(0.95)
                .rotationEffect(Angle(degrees: show ? 5: 0))
//                .rotation3DEffect(Angle(degrees: show ? 30: 0), axis: /*@START_MENU_TOKEN@*/(x: 10.0, y: 10.0, z: 10.0)/*@END_MENU_TOKEN@*/)
                .animation(.interpolatingSpring(mass: 1, stiffness: 100, damping: 10, initialVelocity: 0))
                .onTapGesture {
                    self.show.toggle()
                }
                .gesture(
                    DragGesture()
                        .onChanged { (value) in
                            self.viewState = value.translation
                            self.show = true
                        }
                        .onEnded({ (value) in
                            self.viewState = CGSize.zero
                            self.show = false
                        })
            )
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

struct CardView: View {
    var body: some View {
        VStack {
            Text("Card Back")
            
        }
        .frame(width: 340, height: 220)
    }
}

struct CertificateView: View {
    var body: some View {
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

struct TitleView: View {
    var body: some View {
        VStack {
            HStack {
                Text("Certificates")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                Spacer()
            }
            
            Image("Illustration5")
            Spacer()
        }.padding()
    }
}

struct CardBottomView: View {
    var body: some View {
        VStack(spacing: 20.0) {
            Rectangle()
                .frame(width: 60, height: 6)
                .cornerRadius(3.0)
                .opacity(0.1)
            Text("my test my test my test my test my testmy test my test my test my test")
                .lineLimit(10)
            Spacer()
        }
        .padding()
        .frame(minWidth:0, maxWidth: .infinity)
        .padding(.horizontal)
        .background(Color.white)
        .cornerRadius(30)
        .shadow(radius: 20)
        .offset(y: 600)
    }
}
