#!/usr/bin/env python3
"""
Comprehensive test for the pygame Player class functionality.

This test validates:
1. Player constructor works with pos parameter
2. vx-based horizontal movement
3. Air-strafe functionality 
4. Collision detection and resolution
5. Crouching mechanics
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from widgets import CollideRect, Player

# Disable sound for headless testing
os.environ['SDL_AUDIODRIVER'] = 'dummy'

def test_player_constructor():
    """Test that the Player constructor works with different calling patterns."""
    print("Testing Player constructor...")
    
    # Test with pos parameter (main.py style)
    player1 = Player(
        width=40,
        height=40,
        color=(0, 0, 255),
        fps=60,
        pos=(100, 100),
        speed=200,
    )
    assert player1.x == 100
    assert player1.y == 100
    assert player1.vx == 0.0
    assert player1.vy == 0.0
    print("✓ Constructor with pos parameter works")
    
    # Test with screen_size parameter (collision_testing.py style)
    player2 = Player(
        width=50,
        height=50,
        color=(255, 0, 0),
        pos=(200, 200),
        speed=150,
        screen_size=(800, 600),
    )
    assert player2.x == 200
    assert player2.y == 200
    assert player2.speed == 150
    print("✓ Constructor with screen_size parameter works")

def test_vx_movement():
    """Test that horizontal movement uses vx properly."""
    print("\nTesting vx-based movement...")
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    player = Player(
        width=40,
        height=40,
        pos=(100, 100),
        speed=200,
    )
    
    # Simulate pressing 'D' key (move right)
    player.moving_right = True
    player.moving_left = False
    
    initial_x = player.x
    dt = 1.0 / 60.0  # 60 FPS
    
    player.update(dt, screen)
    
    # Check that vx was set and position updated
    assert player.vx > 0, f"Expected vx > 0, got {player.vx}"
    assert player.x > initial_x, f"Expected player to move right, x went from {initial_x} to {player.x}"
    print(f"✓ Player moved right: vx={player.vx:.1f}, x changed from {initial_x} to {player.x:.1f}")
    
    # Test moving left
    player.moving_right = False
    player.moving_left = True
    
    old_x = player.x
    player.update(dt, screen)
    
    assert player.vx < 0, f"Expected vx < 0, got {player.vx}"
    assert player.x < old_x, f"Expected player to move left, x went from {old_x} to {player.x}"
    print(f"✓ Player moved left: vx={player.vx:.1f}, x changed from {old_x} to {player.x:.1f}")
    
    pygame.quit()

def test_air_strafe():
    """Test that air-strafe functionality works."""
    print("\nTesting air-strafe functionality...")
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    player = Player(
        width=40,
        height=40,
        pos=(100, 100),
        speed=200,
        enable_air_strafing=True,
    )
    
    # Put player in air and start moving
    player.on_ground = False
    player.moving_right = True
    player.moving_left = False
    
    initial_bonus = player.air_strafe_bonus
    dt = 1.0 / 60.0
    
    # Update a few times to build up air-strafe bonus
    for _ in range(10):
        player.update(dt, screen)
    
    assert player.air_strafe_bonus > initial_bonus, f"Expected air_strafe_bonus to increase, got {player.air_strafe_bonus}"
    assert player.strafing == True, "Expected player to be strafing in air"
    print(f"✓ Air-strafe bonus increased from {initial_bonus} to {player.air_strafe_bonus:.3f}")
    
    # Test that bonus doesn't increase when both keys are pressed
    player.moving_right = True
    player.moving_left = True
    
    current_bonus = player.air_strafe_bonus
    player.update(dt, screen)
    
    # When both keys are pressed, strafe bonus should decay, not increase
    assert player.air_strafe_bonus <= current_bonus, "Expected air_strafe_bonus to not increase with both keys pressed"
    print("✓ Air-strafe bonus doesn't increase when both A and D are pressed")
    
    pygame.quit()

def test_collision_resolution():
    """Test that collision detection and resolution works."""
    print("\nTesting collision resolution...")
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    # Create player and platform
    player = Player(
        width=40,
        height=40,
        pos=(200, 200),
        speed=200,
    )
    
    platform = CollideRect(
        screen_size=(800, 600),
        x=220,
        y=220,
        width=100,
        height=20,
        color=(255, 0, 0),
    )
    
    # Move player so it overlaps with platform
    player.x = 225  # This should cause collision
    player.y = 225
    
    assert player.rect.colliderect(platform.rect), "Expected collision between player and platform"
    print("✓ Collision detected")
    
    # Resolve collision
    old_x, old_y = player.x, player.y
    player.resolve_collisions([platform])
    
    # Player should be moved out of collision
    assert not player.rect.colliderect(platform.rect), "Expected collision to be resolved"
    assert (player.x != old_x) or (player.y != old_y), "Expected player position to change"
    print(f"✓ Collision resolved: player moved from ({old_x}, {old_y}) to ({player.x}, {player.y})")
    
    pygame.quit()

def test_crouching():
    """Test that crouching mechanics work."""
    print("\nTesting crouching mechanics...")
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    player = Player(
        width=40,
        height=40,
        pos=(100, 500),
        enable_crouching=True,
        disable_user_controls=True,  # This prevents keyboard override
    )
    
    original_height = player.height
    player.on_ground = True
    player.crouching = True
    
    dt = 1.0 / 60.0
    player.update(dt, screen)
    
    assert player.height < original_height, f"Expected height to decrease when crouching, got {player.height} vs {original_height}"
    print(f"✓ Player height decreased when crouching: {original_height} -> {player.height}")
    
    # Test standing back up
    player.crouching = False
    player.update(dt, screen)
    
    assert player.height == original_height, f"Expected height to return to normal, got {player.height} vs {original_height}"
    print("✓ Player height restored when standing up")
    
    pygame.quit()

def main():
    """Run all tests."""
    print("=== Comprehensive Player Class Test ===")
    
    try:
        test_player_constructor()
        test_vx_movement()
        test_air_strafe()
        test_collision_resolution()
        test_crouching()
        
        print("\n🎉 All tests passed! The Player class is working correctly.")
        print("\nKey features verified:")
        print("  ✓ Constructor supports pos parameter")
        print("  ✓ Horizontal movement uses vx velocity")
        print("  ✓ Air-strafe functionality works")
        print("  ✓ Collision detection and resolution works")
        print("  ✓ Crouching mechanics work")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)