import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { RoundedBox, MeshTransmissionMaterial } from '@react-three/drei';
import * as THREE from 'three';

// Perforation holes for ticket stub tear-off effect
function PerforationHoles() {
  const holes = [];
  const numHoles = 8;
  const spacing = 0.18;
  const startY = -0.63; // Position along left edge

  for (let i = 0; i < numHoles; i++) {
    holes.push(
      <mesh key={i} position={[-1.35, startY + i * spacing, 0.05]}>
        <sphereGeometry args={[0.03, 8, 8]} />
        <meshStandardMaterial 
          color="#3B2A24"
          metalness={0.2}
          roughness={0.8}
        />
      </mesh>
    );
  }
  
  return <>{holes}</>;
}

// Floating ticket with auto-rotation
function RotatingTicket() {
  const ticketRef = useRef();
  
  useFrame((state) => {
    if (ticketRef.current) {
      // Auto-rotate on Y axis
      ticketRef.current.rotation.y += 0.005;
      // Subtle up-down float
      ticketRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.2;
    }
  });

  return (
    <group ref={ticketRef}>
      {/* Main ticket body - wider and flatter like a real ticket */}
      <RoundedBox
        args={[3, 1.4, 0.08]} // width, height, depth - ticket proportions
        radius={0.08}
        smoothness={4}
      >
        {/* Holographic/iridescent material */}
        <meshPhysicalMaterial
          color="#FF8FA3" // Soft coral base color
          metalness={0.3}
          roughness={0.15}
          clearcoat={1}
          clearcoatRoughness={0.1}
          iridescence={1}
          iridescenceIOR={1.3}
          side={THREE.DoubleSide}
        />
      </RoundedBox>
      
      {/* Perforation holes for tear-off stub effect */}
      <PerforationHoles />
      
      {/* Subtle accent line to emphasize the stub separation */}
      <mesh position={[-1.35, 0, 0.045]}>
        <boxGeometry args={[0.02, 1.3, 0.01]} />
        <meshStandardMaterial
          color="#F5B942"
          metalness={0.6}
          roughness={0.3}
          emissive="#F5B942"
          emissiveIntensity={0.3}
        />
      </mesh>
    </group>
  );
}

// Single floating particle
function FloatingParticle({ position, color, speed, amplitude }) {
  const particleRef = useRef();
  const initialY = position[1];
  
  useFrame((state) => {
    if (particleRef.current) {
      // Gentle sine wave motion
      particleRef.current.position.y = 
        initialY + Math.sin(state.clock.elapsedTime * speed) * amplitude;
      
      // Subtle rotation
      particleRef.current.rotation.x += 0.01;
      particleRef.current.rotation.y += 0.01;
    }
  });

  return (
    <mesh ref={particleRef} position={position}>
      <sphereGeometry args={[0.1, 16, 16]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={0.5}
        metalness={0.5}
        roughness={0.3}
      />
    </mesh>
  );
}

// Collection of floating particles
function FloatingParticles() {
  const particles = [
    { position: [-2, 2, -1], color: '#FF6F91', speed: 0.5, amplitude: 0.5 },
    { position: [2, -1, -2], color: '#FF8C42', speed: 0.7, amplitude: 0.6 },
    { position: [-3, -2, 0], color: '#F5B942', speed: 0.6, amplitude: 0.4 },
    { position: [3, 1, -1], color: '#9c27b0', speed: 0.8, amplitude: 0.7 },
    { position: [-1, 3, -2], color: '#FF6F91', speed: 0.4, amplitude: 0.5 },
    { position: [1, -2, -1], color: '#FF8C42', speed: 0.9, amplitude: 0.6 },
    { position: [-2.5, 0, -2], color: '#F5B942', speed: 0.55, amplitude: 0.55 },
    { position: [2.5, 2.5, 0], color: '#ff4081', speed: 0.65, amplitude: 0.45 },
    { position: [0, -3, -1], color: '#FF8C42', speed: 0.75, amplitude: 0.5 },
    { position: [-1.5, 1.5, -2.5], color: '#F5B942', speed: 0.85, amplitude: 0.65 },
    { position: [1.5, -1.5, -1.5], color: '#9c27b0', speed: 0.45, amplitude: 0.4 },
    { position: [0, 2, -3], color: '#FF6F91', speed: 0.7, amplitude: 0.55 },
  ];

  return (
    <>
      {particles.map((particle, index) => (
        <FloatingParticle key={index} {...particle} />
      ))}
    </>
  );
}

// Main 3D scene component
export default function TicketScene() {
  return (
    <div className="w-full h-full relative overflow-hidden">
      {/* Gradient mesh background */}
      <div 
        className="absolute inset-0 bg-gradient-to-br from-[#FF8C42] via-[#FF6F91] to-[#9c27b0]"
        style={{
          filter: 'blur(60px)',
          opacity: 0.6,
        }}
      />
      
      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [0, 0, 8], fov: 50 }}
        className="relative z-10"
      >
        {/* Improved lighting setup - softer and more even */}
        <ambientLight intensity={0.6} />
        <directionalLight position={[5, 5, 5]} intensity={0.5} castShadow />
        <directionalLight position={[-5, -5, -5]} intensity={0.4} />
        {/* Softer point light from further away */}
        <pointLight position={[0, 0, 5]} intensity={0.3} color="#FF8FA3" />
        {/* Additional fill light for even illumination */}
        <pointLight position={[-3, 2, 4]} intensity={0.25} color="#F5B942" />
        <pointLight position={[3, -2, 4]} intensity={0.25} color="#FF8C42" />

        {/* 3D elements */}
        <RotatingTicket />
        <FloatingParticles />
      </Canvas>
    </div>
  );
}
