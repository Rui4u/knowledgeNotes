//
//  UpdateDetail.swift
//  DesignCode
//
//  Created by iOS on 2019/10/25.
//  Copyright © 2019 沙睿. All rights reserved.
//

import SwiftUI

struct UpdateDetail: View {
    var title = "SwiftUI"
    var image = "Illustration2"
    var text = "test"
    var body: some View {
        VStack(spacing: 20.0) {
            Text(title)
                .font(.largeTitle)
                .fontWeight(.heavy)
            Image(image)
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(height:200)
            Text(text)
                .lineLimit(nil)
                .frame(minWidth: 0 ,maxWidth: .infinity, alignment: .leading)
            Spacer()
        }.padding(30)
        
    }
}

struct UpdateDetail_Previews: PreviewProvider {
    static var previews: some View {
        UpdateDetail()
    }
}
