//
//  UpdateStore.swift
//  DesignCode
//
//  Created by iOS on 2019/10/25.
//  Copyright © 2019 沙睿. All rights reserved.
//

import SwiftUI
import Combine

class UpdateStore: ObservableObject {
    var didChange = PassthroughSubject<Void,Never>()
    
    var updates:[Update] {
        didSet {
            didChange.send()
        }
    }
    
    init(updates:[Update] = []) {
        self.updates = updates
    }
}
