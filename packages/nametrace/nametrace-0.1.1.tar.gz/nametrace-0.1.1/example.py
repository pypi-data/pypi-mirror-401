#!/usr/bin/env python3

# nametrace: Human name detection and demographic prediction package.
# Copyright (C) 2025 Paul Bose

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Example usage of the nametrace package."""

from nametrace import NameTracer


def main():
    """Demonstrate the name prediction API."""
    
    # Initialize the tracer (will auto-detect GPU/CPU)
    print("Initializing NameTracer...")
    tracer = NameTracer()
    
    # Example names to test
    test_names = [
        "John Smith",
        "Maria Garcia", 
        "Ahmed Hassan",
        "Li Wei",
        "user123",
        "CompanyName",
        "Sarah Johnson",
        "Fyodor Dostoevsky",
        "randomuser456"
    ]
    
    print("Testing single name predictions...")
    print("=" * 80)
    
    for name in test_names:
        result = tracer.predict(name)
        
        print(f"Name: {name:<20}")
        print(f"  Is Human: {result['is_human']}")
        
        if result['is_human']:
            print(f"  Gender: {result['gender']} (confidence: {result['confidence']['gender']:.3f})")
            print(f"  Region: {result['subregion']} (confidence: {result['confidence']['subregion']:.3f})")
        else:
            print(f"  Human confidence: {result['confidence']['human']:.3f}")
        
        print("-" * 80)
    
    # Top-k prediction example
    print("\nTop-k prediction example (top 3 demographics):")
    result = tracer.predict("Maria Garcia", topk=3)
    print(f"Name: Maria Garcia")
    print(f"  Is Human: {result['is_human']}")
    if result['is_human']:
        print(f"  Genders: {result['gender']}")
        print(f"  Regions: {result['subregion']}")
    print("-" * 80)
    
    # Batch prediction example
    print("\nBatch prediction example:")
    batch_names = ["Anna Kowalski", "tech_user_99", "Mohammed Al-Rashid", "Facebook", "Jennifer Lee"]
    batch_results = tracer.predict(batch_names)
    
    for name, result in zip(batch_names, batch_results):
        status = "HUMAN" if result['is_human'] else "NON-HUMAN"
        print(f"{name:<20} -> {status}")
        if result['is_human']:
            print(f"                     Gender: {result['gender']}, Region: {result['subregion']}")
    
    # Batch with top-k example
    print("\nBatch prediction with top-k (top 2 demographics):")
    human_names = ["Maria Gonzalez", "David Kim", "Priya Sharma"]
    topk_results = tracer.predict(human_names, topk=2)
    
    for name, result in zip(human_names, topk_results):
        print(f"Name: {name}")
        if result['is_human']:
            print(f"  Genders: {result['gender']}")
            print(f"  Regions: {result['subregion']}")
        print()
    
    # Large batch with batch_size example
    print("Large batch with batch_size example:")
    large_batch = [
        "John Doe", "Jane Smith", "user_xyz", "CompanyABC", 
        "Alice Johnson", "Bob Wilson", "admin123", "Chen Wei",
        "Emma Brown", "TechCorporation", "Sarah Davis", "random_user_65"
    ]
    
    # Process in chunks of 4
    chunked_results = tracer.predict(large_batch, batch_size=4)
    
    for name, result in zip(large_batch, chunked_results):
        status = "HUMAN" if result['is_human'] else "NON-HUMAN"
        confidence = result['confidence']['human']
        print(f"{name:<15} -> {status:<10} (conf: {confidence:.3f})")


if __name__ == "__main__":
    main() 